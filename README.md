# Meridian Edge

HTTP routing and session lookup for Meridian workspaces.

Part of the Meridian document workspace. Configuration is supplied through environment variables. SERVICE_KEY authenticates internal requests. The edge resolves sessions through accounts and forwards X-User-Id and X-Tenant-Id to downstream services. Internal services are reachable only on the application network.

## Service peers

- [accounts](https://github.com/sainath1204/meridian-accounts)
- [catalog](https://github.com/sainath1204/meridian-catalog)
- [query](https://github.com/sainath1204/meridian-query)
- [assets](https://github.com/sainath1204/meridian-assets)
- [bundles](https://github.com/sainath1204/meridian-bundles)
- [connectors](https://github.com/sainath1204/meridian-connectors)
- [navigation](https://github.com/sainath1204/meridian-navigation)
- [render](https://github.com/sainath1204/meridian-render)
- [workers](https://github.com/sainath1204/meridian-workers)
