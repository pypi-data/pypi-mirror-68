[![Build Status](https://travis-ci.org/kaelzhang/python-compton.svg?branch=master)](https://travis-ci.org/kaelzhang/python-compton)
[![Coverage](https://codecov.io/gh/kaelzhang/python-compton/branch/master/graph/badge.svg)](https://codecov.io/gh/kaelzhang/python-compton)
<!-- optional appveyor tst
[![Windows Build Status](https://ci.appveyor.com/api/projects/status/github/kaelzhang/python-compton?branch=master&svg=true)](https://ci.appveyor.com/project/kaelzhang/python-compton)
-->
<!-- optional npm version
[![NPM version](https://badge.fury.io/js/python-compton.svg)](http://badge.fury.io/js/python-compton)
-->
<!-- optional npm downloads
[![npm module downloads per month](http://img.shields.io/npm/dm/python-compton.svg)](https://www.npmjs.org/package/python-compton)
-->
<!-- optional dependency status
[![Dependency Status](https://david-dm.org/kaelzhang/python-compton.svg)](https://david-dm.org/kaelzhang/python-compton)
-->

# python-compton

An abstract data-flow framework for quantitative trading, which decouples data initialization, data composition and data processing.

## Install

```sh
pip install compton
```

## Usage

```py
from compton import (
  Orchestrator,
  Provider,
  Reducer,
  Consumer
)
```

## Vector

We call a tuple of hashable parameters as a vector which is used to identify a certain kind of data.

```py
from enum import Enum

class DataType(Enum):
    KLINE = 1
    ORDER_BOOK = 2

class TimeSpan(Enum):
    DAY = 1
    WEEK = 2

vector = (DataType.KLINE, TimeSpan.DAY)
```

## Orchestrator(reducers, loop=None)

- **reducers** `List[Reducer]` reducers to compose data
- **loop** `EventLoop` The event loop object to use

The following code shows how to use compton in a non-coroutine environmennt

```py
loop = asyncio.new_event_loop()

orchestrator = Orchestrator(
    Reducers,
    loop
)

orchestrator.add('US.TSLA')

loop.run_forever()
```

### orchestrator.connect(provider: Provider) -> self

Connects to a data provider

### orchestrator.subscribe(consumer: Consumer) -> self

Subscribes the consumer to orchestrator.

### orchestrator.add(symbol: str) -> self

Adds a new symbol to orchestrator, and start the data flow for `symbol`

## Provider

`Provider` is an abstract class which provides initial data and data updates.

A provider should be implemented to support many symbols

We must inherit class `Provider` and implement some abstract method before use.

- `@property vector` returns an `Vector`
- `async def init()` method returns the initial data
- `def when_update(dispatch)` registers the dispatcher which is a callable.

```py
class MyProvider(Provider):
    @property
    def vector(self):
        return (DataType.KLINE, TimeSpan.DAY)

    def when_update(self, dispatch):
        pass

    async def init(self, symbol):
        return {}
```

## Reducer

Another abstract class which handles data composition.

The `reducer.vector` could be a generic vector which applies partial match to other vectors

```py
class MyReducer(Reducer):
    @property
    def vector(self):
        # So, MyReducer support both
        # - (DataType.KLINE, TimeSpan.DAY)
        # - and (DataType.KLINE, TimeSpan.WEEK)
        return (DataType.KLINE,)

    def merge(self, old, new):
        # `old` might be `None`, if `new` is the initial data
        if old is None:
            # We could clean the initial data
            return clean(new)

        return {**old, **new}
```

## Consumer

A consumer could subscribes to more than one kind of data types

```py
class MyConsumer(Consumer):
    @property
    def vectors(self):
        # Subscribe to two kinds of data types
        return [
            (DataType.KLINE, TimeSpan.DAY),
            (DataType.KLINE, TimeSpan.WEEK)
        ]

    @property
    def all(self):
        # `True` indicates that the consumer will only go processing
        # if both of the data corresponds with the two vectors have changes

        # And by default, `Consumer::all` is False
        return True

    @property
    def concurrency(self):
        # concurrency limit for method `process()`

        # By default, `Consumer::concurrency` is `0` which means no limit
        return 1

    # Then there will be
    # both `kline_day` and `kline_week` passed into method `process`
    async def process(self, symbol, kline_day, kline_week):
        await doSomething(symbol, kline_day, kline_week)
```

## License

[MIT](LICENSE)
