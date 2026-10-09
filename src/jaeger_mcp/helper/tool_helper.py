import logging
import os
from datetime import UTC, datetime, timedelta

import requests
from dotenv import find_dotenv, load_dotenv

from jaeger_mcp.schemas import services, traces

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

SERVICE_API_VERSION = os.getenv("SERVICE_API_VERSION", "v3")


def ping_jaeger(ping_url: str) -> str:
    try:
        logger.info(f"testing {ping_url}")
        response = requests.get(ping_url)
        if response.status_code == 200:
            logger.info(f"{ping_url} is active")
            return f"jaeger accessible on {ping_url}"
        else:
            logger.warning(f"{ping_url} is down")
            return f"cannot connect to jaeger on {ping_url}"
    except Exception as e:
        logger.error(f"raised exception here for {ping_url} : {e!s}")
        return f"cannot connect to jaeger on {ping_url} , maybe jaeger is not deployed"


def get_all_services(ping_url: str) -> services.GetAllServices | str:
    try:
        service_url = f"{ping_url}/api/{SERVICE_API_VERSION}/services"
        logger.info(f"getting services for {service_url}")
        response = requests.get(service_url)
        logging.info(f"{response.json()}")
        if response.status_code == 200:
            logger.info(f"{service_url} is active")
            body = response.json()
            return services.GetAllServices(services=body.get("services", []))
        else:
            logger.warning(f"{service_url} is down")
            return f"cannot connect to jaeger on {service_url}"
    except Exception as e:
        logger.error(f"raised exception here for {service_url} : {e!s}")
        return (
            f"cannot connect to jaeger on {service_url} , maybe jaeger is not deployed"
        )


def get_service_operations(
    ping_url: str, service_name: str
) -> services.GetServiceOperations | str:
    try:
        service_url = (
            f"{ping_url}/api/{SERVICE_API_VERSION}/operations?service={service_name}"
        )
        logger.info(f"getting services for {service_url}")
        response = requests.get(service_url)
        logging.info(f"{response.json()}")
        if response.status_code == 200:
            logger.info(f"{service_url} is active")
            body = response.json()
            operations = []
            for itr in body.get("operations", {}):
                operations.append(
                    services.Operation(
                        name=itr.get("name", ""), spanKind=itr.get("spanKind", "")
                    )
                )
            return services.GetServiceOperations(operations=operations)
        else:
            logger.warning(f"{service_url} is down")
            return f"cannot connect to jaeger on {service_url}"
    except Exception as e:
        logger.error(f"raised exception here for {service_url} : {e!s}")
        return (
            f"cannot connect to jaeger on {service_url} , maybe jaeger is not deployed"
        )


def get_trace_summaries(
    ping_url: str,
    service_name: str,
    start_time_min: str | None = None,
    start_time_max: str | None = None,
    search_depth: int = 20,
    operation_name: str | None = None,
) -> traces.GetTraceSummaries | str:
    try:
        service_url = f"{ping_url}/api/{SERVICE_API_VERSION}/trace-summaries"

        if not start_time_max:
            start_time_max = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if not start_time_min:
            start_time_min = (datetime.now(UTC) - timedelta(hours=1)).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )

        params: dict[str, str | int] = {
            "query.serviceName": service_name,
            "query.startTimeMin": start_time_min,
            "query.startTimeMax": start_time_max,
            "query.searchDepth": search_depth,
        }
        if operation_name:
            params["query.operationName"] = operation_name

        logger.info(f"getting trace summaries for {service_url} with params {params}")
        response = requests.get(service_url, params=params)
        logger.info(f"{response.status_code}")
        if response.status_code == 200:
            logger.info(f"{service_url} is active")
            body = response.json()
            summaries = []
            for item in body.get("summaries", []):
                svc_list = [
                    traces.ServiceSummary(
                        name=s.get("name", ""), spanCount=s.get("spanCount", 0)
                    )
                    for s in item.get("services", [])
                ]
                summaries.append(
                    traces.TraceSummary(
                        traceId=item.get("traceId", ""),
                        rootServiceName=item.get("rootServiceName", ""),
                        rootOperationName=item.get("rootOperationName", ""),
                        minStartTimeUnixNano=str(item.get("minStartTimeUnixNano", "")),
                        maxEndTimeUnixNano=str(item.get("maxEndTimeUnixNano", "")),
                        spanCount=item.get("spanCount", 0),
                        services=svc_list,
                    )
                )
            return traces.GetTraceSummaries(summaries=summaries)
        else:
            logger.warning(f"{service_url} is down")
            return f"cannot connect to jaeger on {service_url}"
    except Exception as e:
        logger.error(f"raised exception here for {service_url} : {e!s}")
        return (
            f"cannot connect to jaeger on {service_url} , maybe jaeger is not deployed"
        )


def _fetch_raw_trace(ping_url: str, trace_id: str) -> tuple[dict | None, str | None]:
    url = f"{ping_url}/api/traces/{trace_id}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            return data, None
        return (
            None,
            f"Jaeger returned status {resp.status_code} for trace {trace_id} at {url}",
        )
    except Exception as e:
        return None, f"Failed to connect to Jaeger on {url}: {e!s}"


def _parse_trace_spans(raw_data: dict, trace_id: str = "") -> list[dict]:
    spans: list[dict] = []
    for item in raw_data.get("data", []):
        processes = item.get("processes", {})
        for s in item.get("spans", []):
            service_name = processes.get(s.get("processID", ""), {}).get(
                "serviceName", "unknown"
            )
            tags = {t["key"]: t["value"] for t in s.get("tags", []) if "key" in t}

            parent_id = None
            for r in s.get("references", []):
                if r.get("refType") == "CHILD_OF":
                    parent_id = r.get("spanID")
                    break

            start_us = int(s.get("startTime", 0) or 0)
            duration_us = int(s.get("duration", 0) or 0)
            end_us = start_us + duration_us
            duration_ms = round(duration_us / 1000.0, 3)
            is_err = (
                tags.get("error") is True
                or int(tags.get("http.status_code", 0) or 0) >= 400
            )

            spans.append(
                {
                    "spanId": s.get("spanID", ""),
                    "parentSpanId": parent_id,
                    "serviceName": service_name,
                    "operationName": s.get("operationName", ""),
                    "startTimeUnixNano": str(start_us * 1000),
                    "endTimeUnixNano": str(end_us * 1000),
                    "startNs": start_us * 1000,
                    "endNs": end_us * 1000,
                    "durationMs": duration_ms,
                    "statusCode": "ERROR" if is_err else "OK",
                    "statusMessage": "",
                    "isError": is_err,
                    "attributes": tags,
                    "events": s.get("logs", []),
                }
            )
    return spans


def get_trace_overview(ping_url: str, trace_id: str) -> traces.TraceOverview | str:
    try:
        raw_data, err = _fetch_raw_trace(ping_url, trace_id)
        if err or not raw_data:
            return err or f"No trace found for ID {trace_id}"

        spans = _parse_trace_spans(raw_data, trace_id)
        if not spans:
            return f"Trace {trace_id} contains no spans"

        min_start = min(s["startNs"] for s in spans)
        max_end = max(s["endNs"] for s in spans)
        total_duration_ms = (
            round((max_end - min_start) / 1_000_000.0, 3)
            if max_end >= min_start
            else max(s["durationMs"] for s in spans)
        )

        span_ids = {s["spanId"] for s in spans}
        roots = [s for s in spans if s["parentSpanId"] not in span_ids]
        root_span = roots[0] if roots else spans[0]

        service_map: dict[str, dict] = {}
        for s in spans:
            svc = s["serviceName"]
            if svc not in service_map:
                service_map[svc] = {
                    "spanCount": 0,
                    "cumulativeDurationMs": 0.0,
                    "errorCount": 0,
                }
            service_map[svc]["spanCount"] += 1
            service_map[svc]["cumulativeDurationMs"] += s["durationMs"]
            if s["isError"]:
                service_map[svc]["errorCount"] += 1

        service_metrics = [
            traces.ServiceMetrics(
                serviceName=k,
                spanCount=v["spanCount"],
                cumulativeDurationMs=round(v["cumulativeDurationMs"], 3),
                errorCount=v["errorCount"],
            )
            for k, v in service_map.items()
        ]

        error_count = sum(1 for s in spans if s["isError"])

        return traces.TraceOverview(
            traceId=trace_id,
            rootServiceName=root_span["serviceName"],
            rootOperationName=root_span["operationName"],
            totalDurationMs=total_duration_ms,
            spanCount=len(spans),
            errorCount=error_count,
            hasErrors=error_count > 0,
            services=service_metrics,
        )
    except Exception as e:
        logger.error(f"Error getting trace overview for {trace_id}: {e!s}")
        return f"Error retrieving trace overview for {trace_id}: {e!s}"


def get_slowest_spans(
    ping_url: str,
    trace_id: str,
    limit: int = 10,
    offset: int = 0,
) -> traces.GetSlowestSpans | str:
    try:
        raw_data, err = _fetch_raw_trace(ping_url, trace_id)
        if err or not raw_data:
            return err or f"No trace found for ID {trace_id}"

        spans = _parse_trace_spans(raw_data, trace_id)
        if not spans:
            return f"Trace {trace_id} contains no spans"

        if offset + limit > len(spans):
            return "offset + limit is beyond the number of spans"

        sorted_spans = sorted(spans, key=lambda s: s["durationMs"], reverse=True)
        total_spans = len(sorted_spans)

        paged_spans = sorted_spans[offset : offset + limit]
        has_more = (offset + limit) < total_spans

        result_spans = [
            traces.SlowestSpan(
                spanId=s["spanId"],
                parentSpanId=s.get("parentSpanId"),
                serviceName=s["serviceName"],
                operationName=s["operationName"],
                durationMs=s["durationMs"],
                statusCode=s["statusCode"],
                isError=s["isError"],
            )
            for s in paged_spans
        ]

        return traces.GetSlowestSpans(
            traceId=trace_id,
            totalSpans=total_spans,
            limit=limit,
            offset=offset,
            hasMore=has_more,
            spans=result_spans,
        )
    except Exception as e:
        logger.error(f"Error getting slowest spans for {trace_id}: {e!s}")
        return f"Error retrieving slowest spans for {trace_id}: {e!s}"


def get_trace_errors(ping_url: str, trace_id: str) -> traces.TraceErrors | str:
    try:
        raw_data, err = _fetch_raw_trace(ping_url, trace_id)
        if err or not raw_data:
            return err or f"No trace found for ID {trace_id}"

        spans = _parse_trace_spans(raw_data, trace_id)
        if not spans:
            return f"Trace {trace_id} contains no spans"

        error_spans = [s for s in spans if s["isError"]]
        errors_list: list[traces.TraceErrorSpan] = []

        for s in error_spans:
            error_attrs = {
                k: v
                for k, v in s["attributes"].items()
                if any(
                    term in k.lower()
                    for term in (
                        "error",
                        "status",
                        "exception",
                        "http.",
                        "rpc.",
                        "message",
                    )
                )
            }
            errors_list.append(
                traces.TraceErrorSpan(
                    spanId=s["spanId"],
                    serviceName=s["serviceName"],
                    operationName=s["operationName"],
                    durationMs=s["durationMs"],
                    statusCode=s["statusCode"],
                    statusMessage=s["statusMessage"],
                    errorAttributes=error_attrs,
                    events=s["events"],
                )
            )

        return traces.TraceErrors(
            traceId=trace_id,
            totalErrors=len(errors_list),
            errors=errors_list,
        )
    except Exception as e:
        logger.error(f"Error getting trace errors for {trace_id}: {e!s}")
        return f"Error retrieving trace errors for {trace_id}: {e!s}"


def get_span_details(
    ping_url: str, trace_id: str, span_id: str
) -> traces.SpanDetails | str:
    try:
        raw_data, err = _fetch_raw_trace(ping_url, trace_id)
        if err or not raw_data:
            return err or f"No trace found for ID {trace_id}"

        spans = _parse_trace_spans(raw_data, trace_id)
        target_span = [s for s in spans if s["spanId"] == span_id]

        if len(target_span) == 0:
            return f"Span {span_id} not found in trace {trace_id}"

        target_span = target_span[0]

        child_ids = [
            s["spanId"] for s in spans if s.get("parentSpanId") == target_span["spanId"]
        ]

        return traces.SpanDetails(
            traceId=trace_id,
            spanId=target_span["spanId"],
            parentSpanId=target_span.get("parentSpanId"),
            serviceName=target_span["serviceName"],
            operationName=target_span["operationName"],
            startTimeUnixNano=target_span["startTimeUnixNano"],
            endTimeUnixNano=target_span["endTimeUnixNano"],
            durationMs=target_span["durationMs"],
            statusCode=target_span["statusCode"],
            statusMessage=target_span["statusMessage"],
            isError=target_span["isError"],
            attributes=target_span["attributes"],
            events=target_span["events"],
            childSpanIds=child_ids,
        )
    except Exception as e:
        logger.error(f"Error getting span details for {span_id}: {e!s}")
        return f"Error retrieving span details for {span_id}: {e!s}"
