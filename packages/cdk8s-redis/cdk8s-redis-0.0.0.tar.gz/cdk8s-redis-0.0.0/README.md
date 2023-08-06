# cdk8s-redis

> Redis constructs for cdk8s

Basic implementation of a Redis construct for cdk8s. Contributions are welcome!

## Usage

The following will define a Redis cluster with a master and 2 slave replicas:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk8s_redis import Redis

# inside your chart:
redis = Redis(self, "my-redis")
```

DNS names can be obtained from `redis.masterHost` and `redis.slaveHost`.

You can specify how many slave replicas to define:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Redis(self, "my-redis",
    slave_replicas=4
)
```

Or, you can specify no slave:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Redis(self, "my-redis",
    slave_replicas=0
)
```

## License

Distributed under the [Apache 2.0](./LICENSE) license.
