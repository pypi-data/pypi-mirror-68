# graphene-prometheus

📊 Prometheus exporter middleware for the Graphene GraphQL framework.

_This is still under development. Use at your own risk._

## Usage

Install using `pip install graphene-prometheus` or `poetry add graphene-prometheus`.

### Graphene

```python
import graphene_prometheus

schema.execute("THE QUERY", middleware=[graphene_prometheus.PrometheusMiddleware()])
```

See https://docs.graphene-python.org/en/latest/execution/middleware/#middleware for more information.

### Django

In `settings.py`:

```python
GRAPHENE = {
    "MIDDLEWARE": ["graphene_prometheus.PrometheusMiddleware"],
}
```

See https://docs.graphene-python.org/projects/django/en/latest/settings/#middleware for more information.

### FastAPI / Starlette

Coming soon.
