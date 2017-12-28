# PyMineHub

## Target version

- Python 3.5.3
  - 2017-09-07-raspbian-stretch-lite.img

## Development

### Module design

#### Dependency

Modules depend only on parents or siblings. Siblings depend only on the above siblings.

```
typevar
config -> typevar
value -> config
binutil -> typevar
  converter -> typevar
  instance -> .[converter]
  composite -> typevar, .[converter]
network -> binutil
  address
  codec -> value, binutil.[composite, instance], .[address]
raknet -> value, config, network
  - fragment -> value
  - packet -> value, network.[address]
  - frame -> .[packet]
  - codec -> network.[codec], .[frame, packet]
  - sending -> config, value, .[codec, frame]
  - session -> value, .[codec, fragment, frame, packet, queue]
  - server -> config, value, network.[address, codec], .[codec, packet, frame, session]
mcpe
  const
  geometry -> typevar
  value -> binutil.[converter], .[const, geometry]
  resource
    - loader
  metadata -> .[const, geometry, value]
  inventory -> mcpe.[resource], .[const, value]
  command -> .[const, value]
  chunk -> binutil.[composite, instance], mcpe.[const, geometry]
  player -> .[value]
  plugin
    generator -> mcpe.[geometry, chunk]
    default
      - generator -> mcpe.[chunk], mcpe.plugin.[generator]
    loader -> .[generator, default]
  world -> value, .[const, player]
    - action -> value, mcpe.[player]
    - event -> value, mcpe.[player]
    - database -> config, mcpe.[geometry, chunk]
    - generator -> mcpe.[geometry, chunk, plugin], .[database]
    - space -> mcpe.[geometry, chunk], .[database, generator]
    - proxy -> mcpe.[const, value, resource], .[action, event]
    - server -> mcpe.[inventory, chunk], .[database, generator, space, proxy]
  network -> typevar, value, config, network, raknet, mcpe.[const, value, metadata, player, world]
    - packet -> value, mcpe.[value], network.[address]
    - codec -> typevar, config, network, .[packet]
      - batch -> typevar, network.[codec], mcpe.network.[packet]
      - connection -> config, network.[codec], mcpe.network.[packet]
    - queue -> value, raknet, network.[address], .[packet, codec]
    - handler -> typevar, value, raknet, network.[address],
                 mcpe.[const, metadata, command, player, world], .[codec, packet, queue]
  main
    server -> raknet, mcpe.[network, world]

- : Hidden from outside modules
```

### Reference

- This project is implemented by referring to [PocketMine-MP](https://github.com/pmmp/PocketMine-MP) source code.
- [RakNet](http://www.raknet.net/raknet/manual/systemoverview.html)
- [Pocket Edition Protocol Documentation](http://wiki.vg/Pocket_Edition_Protocol_Documentation)
