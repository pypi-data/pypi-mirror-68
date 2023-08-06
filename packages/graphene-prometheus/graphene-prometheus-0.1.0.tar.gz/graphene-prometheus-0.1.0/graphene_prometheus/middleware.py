from typing import Any, Callable, Optional

import graphene
from prometheus_client import Counter, Histogram

GRAPHQL_RESOLVER_LATENCY_SECONDS = Histogram(
    "graphql_resolver_latency_seconds",
    "Histogram of time taken for a resolver to complete.",
    ["operation_type", "field"],
)
GRAPHQL_RESOLVER_EXCEPTIONS_TOTAL = Counter(
    "graphql_resolver_exceptions_total",
    "Total exceptions raised by a resolver.",
    ["operation_type", "field"],
)
GRAPHQL_RESOLVER_COMPLETED_TOTAL = Counter(
    "graphql_resolver_completed_total",
    "Total resolver completed.",
    ["operation_type", "field"],
)


class PrometheusMiddleware:
    def resolve(
        self,
        next: Callable,
        root: Optional[graphene.Schema],
        info: graphene.ResolveInfo,
        **args: Any
    ) -> Any:
        with GRAPHQL_RESOLVER_LATENCY_SECONDS.labels(
            operation_type=info.operation.operation, field=info.field_name,
        ).time():
            with GRAPHQL_RESOLVER_EXCEPTIONS_TOTAL.labels(
                operation_type=info.operation.operation, field=info.field_name,
            ).count_exceptions():
                return_value = next(root, info, **args)
        GRAPHQL_RESOLVER_COMPLETED_TOTAL.labels(
            operation_type=info.operation.operation, field=info.field_name,
        ).inc()
        return return_value
