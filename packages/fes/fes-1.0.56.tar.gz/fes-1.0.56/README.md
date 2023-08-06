# Finac Enterprise Server

https://www.altertech.com/products/fes/

Configuration example:

```yaml
fes:
  key: secret
  real-ip-header: X-Real-IP
  finac:
    db: postgresql://finac:PASSWORD@HOST/finac
    db-pool-size: 30
    redis-host: localhost
    multiplier: 1000
    restrict-deletion: 1
    lazy-exchange: false
    rate-allow-reverse: true
    rate-allow-cross: true
    base-asset: EUR
  gunicorn:
    listen: 0.0.0.0:8832
    #gunicorn: gunicorn3
    pid-file: /tmp/fes.pid
    start-failed-after: 5
    force-stop-after: 10
    launch-debug: true
    extra-options: -w 2 --log-file /var/log/fes/fes.log --log-level INFO -u fes
```
