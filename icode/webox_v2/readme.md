
## todo
- st.Page / st.navigation (not show)
- switch to page tabs
- empty model
- model.__str__

## project

```python

libx
    libdns
        dns_app

webox
    common
        cache.py        # gcache, global cache
        config.py       # gconf,  global config
        const.py        # gconst, global const
        state.py        # gst,    global session state
        page.py
    dns
        common
            dns_const.py
            dns_state.py
            dns_service.py
        ist
        idy
            page
                wideip_list.py
                wideip_detail.py
                wideip_create.py
                wideip_update.py
                pool_list.py
                pool_detail.py
                pool_create.py
                pool_update.py
            view
                wideip.py
                pool.py

# dns/common/dns_const.py
# import dns.common.dns_const as dnsc
class Pages():
    ist_record_create = "dns/ist/page/record_create.py"

# dns/common/dns_state.py
class DnsState():
    pass

dnst = DnsState()

# dns/common/dns_service.py
class DnsService():
    def app():
        return DnsApp()

dnss = DnsService()

# dns/idy/view/wideip.py
dnss.app.idy.nsp.create_wideip()
dnss.app.idy.repo.get_wideip()
```

dnsc
dnst
dnss

v5sc
v5st
v5ss
