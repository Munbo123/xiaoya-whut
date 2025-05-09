!function(t) {
    "use strict";
    function e(t, e, n) {
        Object.defineProperty(t, e, {
            writable: !0,
            enumerable: !0,
            configurable: !0,
            value: n
        })
    }
    function n(t, n, r, o) {
        o ? o(( () => {
            e(t, n, r)
        }
        )) : e(t, n, r)
    }
    class r {
        constructor(t) {
            this.onFirstSubscribe = t,
            this.observers = []
        }
        subscribe(t) {
            return !this.observers.length && this.onFirstSubscribe && (this.onLastUnsubscribe = this.onFirstSubscribe() || void 0),
            this.observers.push(t),
            {
                unsubscribe: () => {
                    this.observers = this.observers.filter((e => t !== e)),
                    !this.observers.length && this.onLastUnsubscribe && this.onLastUnsubscribe()
                }
            }
        }
        notify(t) {
            this.observers.forEach((e => e(t)))
        }
    }
    function o(t, e, n) {
        try {
            return t.apply(e, n)
        } catch (r) {
            return
        }
    }
    function i(t) {
        return function() {
            return o(t, this, arguments)
        }
    }
    var s = Object.defineProperty
      , a = Object.defineProperties
      , c = Object.getOwnPropertyDescriptors
      , u = Object.getOwnPropertySymbols
      , l = Object.prototype.hasOwnProperty
      , p = Object.prototype.propertyIsEnumerable
      , f = (t, e, n) => e in t ? s(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , d = (t, e) => {
        for (var n in e || (e = {}))
            l.call(e, n) && f(t, n, e[n]);
        if (u)
            for (var n of u(e))
                p.call(e, n) && f(t, n, e[n]);
        return t
    }
      , h = (t, e) => a(t, c(e));
    const m = "0.3.5";
    function b(t) {
        return "number" == typeof t
    }
    function g(t, e) {
        return +t.toFixed(e)
    }
    function O(t, e) {
        return -1 !== t.indexOf(e)
    }
    function R(t, e) {
        return null == t ? e : !!t
    }
    function y(t) {
        return t ? (parseInt(t, 10) ^ 16 * Math.random() >> parseInt(t, 10) / 4).toString(16) : "10000000-1000-4000-8000-100000000000".replace(/[018]/g, y)
    }
    function E(t, e) {
        return (...n) => {
            try {
                return t(...n)
            } catch (r) {
                console.error(e, r)
            }
        }
    }
    function v(t, e) {
        return t.includes("/track?APIVersion=0.6.0") || t === function(t) {
            let e;
            return e = t.host.startsWith("http://") || t.host.startsWith("https://") ? t.host + "/logstores/" + t.logstore + (t.stsPlugin ? "" : "/track?APIVersion=0.6.0") : "https://" + t.project + "." + t.host + "/logstores/" + t.logstore + (t.stsPlugin ? "" : "/track?APIVersion=0.6.0"),
            e
        }(e)
    }
    const S = /^(?:([^:\/?#]+):\/\/)?((?:([^\/?#@]*)@)?([^\/?#:]*)(?:\:(\d*))?)?([^?#]*)(?:\?([^#]*))?(?:#((?:.|\n)*))?/i;
    function w(t) {
        var e = function(t) {
            try {
                return decodeURIComponent(t)
            } catch (e) {
                return unescape(t)
            }
        }(t || "").match(S);
        if (null == e)
            return null;
        var n = (e[3] || "").split(":")
          , r = n.length ? (e[2] || "").replace(/(.*\@)/, "") : e[2];
        return {
            uri: e[0],
            protocol: e[1],
            host: r,
            hostname: e[4],
            port: e[5],
            auth: e[3],
            user: n[0],
            password: n[1],
            path: e[6],
            search: e[7],
            hash: e[8]
        }
    }
    function T(t, e, n, r) {
        const o = {
            url: t,
            method: e,
            status_code: n
        };
        return null == r ? o : h(d({}, o), {
            host: r.host,
            scheme: r.protocol
        })
    }
    function _(t, e, ...n) {
        return !(null == e || !Array.isArray(e)) && e.some((e => {
            if ("function" == typeof e)
                try {
                    return e(t, ...n)
                } catch (r) {
                    return console.error("user function callback threw an error:", r),
                    !1
                }
            return "string" == typeof e ? t.includes(e) : "[object RegExp]" === Object.prototype.toString.call(e) && e.test(t)
        }
        ))
    }
    function I(t, e) {
        return null == e || _(t, e)
    }
    function P(t, e, n) {
        return !1 !== t && (!0 === t || ("error" === t && !n || "function" == typeof t && E(t, "call shouldTrackBody failed")(e)))
    }
    function x(t) {
        return {
            relative: t,
            timeStamp: B(t)
        }
    }
    function B(t) {
        const e = Date.now() - performance.now();
        return e > A() ? Math.round(e + t) : function(t) {
            return Math.round(A() + t)
        }(t)
    }
    function C(t) {
        return b(t) ? g(1e6 * t, 0) : t
    }
    function L() {
        return Date.now()
    }
    function N() {
        return performance.now()
    }
    function k(t, e) {
        return e - t
    }
    let j;
    function A() {
        return void 0 === j && (j = performance.timing.navigationStart),
        j
    }
    const M = "?";
    function $(t, e) {
        let n;
        const r = void 0 === e ? 0 : +e;
        try {
            if (n = function(t) {
                const e = D(t, "stacktrace");
                if (!e)
                    return;
                const n = / line (\d+).*script (?:in )?(\S+)(?:: in function (\S+))?$/i
                  , r = / line (\d+), column (\d+)\s*(?:in (?:<anonymous function: ([^>]+)>|([^)]+))\((.*)\))? in (.*):\s*$/i
                  , o = e.split("\n")
                  , i = [];
                let s;
                for (let a = 0; a < o.length; a += 2) {
                    let t;
                    n.exec(o[a]) ? (s = n.exec(o[a]),
                    t = {
                        args: [],
                        column: void 0,
                        func: s[3],
                        line: +s[1],
                        url: s[2]
                    }) : r.exec(o[a]) && (s = r.exec(o[a]),
                    t = {
                        args: s[5] ? s[5].split(",") : [],
                        column: +s[2],
                        func: s[3] || s[4],
                        line: +s[1],
                        url: s[6]
                    }),
                    t && (!t.func && t.line && (t.func = M),
                    t.context = [o[a + 1]],
                    i.push(t))
                }
                if (!i.length)
                    return;
                return {
                    stack: i,
                    message: D(t, "message"),
                    name: D(t, "name")
                }
            }(t),
            n)
                return n
        } catch (o) {}
        try {
            if (n = function(t) {
                const e = D(t, "stack");
                if (!e)
                    return;
                const n = /^\s*at (.*?) ?\(((?:file|https?|blob|chrome-extension|native|eval|webpack|<anonymous>|\/).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i
                  , r = /^\s*(.*?)(?:\((.*?)\))?(?:^|@)((?:file|https?|blob|chrome|webpack|resource|capacitor|\[native).*?|[^@]*bundle)(?::(\d+))?(?::(\d+))?\s*$/i
                  , o = /^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|webpack|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i;
                let i;
                const s = /(\S+) line (\d+)(?: > eval line \d+)* > eval/i
                  , a = /\((\S*)(?::(\d+))(?::(\d+))\)/
                  , c = e.split("\n")
                  , u = [];
                let l, p, f;
                for (let d = 0, h = c.length; d < h; d += 1) {
                    if (n.exec(c[d])) {
                        p = n.exec(c[d]);
                        const t = p[2] && 0 === p[2].indexOf("native");
                        i = p[2] && 0 === p[2].indexOf("eval"),
                        l = a.exec(p[2]),
                        i && l && (p[2] = l[1],
                        p[3] = l[2],
                        p[4] = l[3]),
                        f = {
                            args: t ? [p[2]] : [],
                            column: p[4] ? +p[4] : void 0,
                            func: p[1] || M,
                            line: p[3] ? +p[3] : void 0,
                            url: t ? void 0 : p[2]
                        }
                    } else if (o.exec(c[d]))
                        p = o.exec(c[d]),
                        f = {
                            args: [],
                            column: p[4] ? +p[4] : void 0,
                            func: p[1] || M,
                            line: +p[3],
                            url: p[2]
                        };
                    else {
                        if (!r.exec(c[d]))
                            continue;
                        p = r.exec(c[d]),
                        i = p[3] && p[3].indexOf(" > eval") > -1,
                        l = s.exec(p[3]),
                        i && l ? (p[3] = l[1],
                        p[4] = l[2],
                        p[5] = void 0) : 0 !== d || p[5] || H(t.columnNumber) || (u[0].column = t.columnNumber + 1),
                        f = {
                            args: p[2] ? p[2].split(",") : [],
                            column: p[5] ? +p[5] : void 0,
                            func: p[1] || M,
                            line: p[4] ? +p[4] : void 0,
                            url: p[3]
                        }
                    }
                    !f.func && f.line && (f.func = M),
                    u.push(f)
                }
                if (!u.length)
                    return;
                return {
                    stack: u,
                    message: D(t, "message"),
                    name: D(t, "name")
                }
            }(t),
            n)
                return n
        } catch (o) {}
        try {
            if (n = function(t) {
                const e = D(t, "message");
                if (!e)
                    return;
                const n = e.split("\n");
                if (n.length < 4)
                    return;
                const r = /^\s*Line (\d+) of linked script ((?:file|https?|blob)\S+)(?:: in function (\S+))?\s*$/i
                  , o = /^\s*Line (\d+) of inline#(\d+) script in ((?:file|https?|blob)\S+)(?:: in function (\S+))?\s*$/i
                  , i = /^\s*Line (\d+) of function script\s*$/i
                  , s = []
                  , a = window && window.document && window.document.getElementsByTagName("script")
                  , c = [];
                let u;
                for (const l in a)
                    W(a, l) && !a[l].src && c.push(a[l]);
                for (let l = 2; l < n.length; l += 2) {
                    let t;
                    if (r.exec(n[l]))
                        u = r.exec(n[l]),
                        t = {
                            args: [],
                            column: void 0,
                            func: u[3],
                            line: +u[1],
                            url: u[2]
                        };
                    else if (o.exec(n[l]))
                        u = o.exec(n[l]),
                        t = {
                            args: [],
                            column: void 0,
                            func: u[4],
                            line: +u[1],
                            url: u[3]
                        };
                    else if (i.exec(n[l])) {
                        u = i.exec(n[l]);
                        t = {
                            url: window.location.href.replace(/#.*$/, ""),
                            args: [],
                            column: void 0,
                            func: "",
                            line: +u[1]
                        }
                    }
                    t && (t.func || (t.func = M),
                    t.context = [n[l + 1]],
                    s.push(t))
                }
                if (!s.length)
                    return;
                return {
                    stack: s,
                    message: n[0],
                    name: D(t, "name")
                }
            }(t),
            n)
                return n
        } catch (o) {}
        try {
            if (n = U(t, r + 1),
            n)
                return n
        } catch (o) {}
        return {
            message: D(t, "message"),
            name: D(t, "name"),
            stack: []
        }
    }
    function U(t, e) {
        const n = /function\s+([_$a-zA-Z\xA0-\uFFFF][_$a-zA-Z0-9\xA0-\uFFFF]*)?\s*\(/i
          , r = []
          , o = {};
        let i, s, a = !1;
        for (let u = U.caller; u && !a; u = u.caller)
            u !== $ && (s = {
                args: [],
                column: void 0,
                func: M,
                line: void 0,
                url: void 0
            },
            i = n.exec(u.toString()),
            u.name ? s.func = u.name : i && (s.func = i[1]),
            void 0 === s.func && (s.func = i ? i.input.substring(0, i.input.indexOf("{")) : void 0),
            o[u.toString()] ? a = !0 : o[u.toString()] = !0,
            r.push(s));
        e && r.splice(0, e);
        const c = {
            stack: r,
            message: D(t, "message"),
            name: D(t, "name")
        };
        return function(t, e, n) {
            const r = {
                url: e,
                line: n ? +n : void 0
            };
            if (r.url && r.line) {
                t.incomplete = !1;
                const e = t.stack;
                if (e.length > 0 && e[0].url === r.url) {
                    if (e[0].line === r.line)
                        return !1;
                    if (!e[0].line && e[0].func === r.func)
                        return e[0].line = r.line,
                        e[0].context = r.context,
                        !1
                }
                return e.unshift(r),
                t.partial = !0,
                !0
            }
            t.incomplete = !0
        }(c, D(t, "sourceURL") || D(t, "fileName"), D(t, "line") || D(t, "lineNumber")),
        c
    }
    function D(t, e) {
        if ("object" != typeof t || !t || !(e in t))
            return;
        const n = t[e];
        return "string" == typeof n ? n : void 0
    }
    function W(t, e) {
        return Object.prototype.hasOwnProperty.call(t, e)
    }
    function H(t) {
        return void 0 === t
    }
    function F(t, e, n) {
        const r = t[e];
        let o = n(r);
        const i = function() {
            return o.apply(this, arguments)
        };
        return t[e] = i,
        {
            stop: () => {
                t[e] === i ? t[e] = r : o = r
            }
        }
    }
    function q(t, e, {before: n, after: r}) {
        return F(t, e, (t => function() {
            const e = arguments;
            let i;
            return n && o(n, this, e),
            "function" == typeof t && (i = t.apply(this, e)),
            r && o(r, this, e),
            i
        }
        ))
    }
    const z = /^(?:[Uu]ncaught (?:exception: )?)?(?:((?:Eval|Internal|Range|Reference|Syntax|Type|URI|)Error): )?(.*)$/;
    function G(t) {
        const {stop: e} = function(t) {
            return q(window, "onerror", {
                before(e, n, r, o, i) {
                    let s;
                    if (i)
                        s = $(i),
                        t(s, i);
                    else {
                        const i = {
                            url: n,
                            column: o,
                            line: r
                        };
                        let a, c = e;
                        if ("[object String]" === {}.toString.call(e)) {
                            const t = z.exec(c);
                            t && (a = t[1],
                            c = t[2])
                        }
                        s = {
                            name: a,
                            message: "string" == typeof c ? c : void 0,
                            stack: [i]
                        },
                        t(s, e)
                    }
                }
            })
        }(t)
          , {stop: n} = function(t) {
            return q(window, "onunhandledrejection", {
                before(e) {
                    const n = e.reason || "Empty reason"
                      , r = $(n);
                    t(r, n)
                }
            })
        }(t);
        return {
            stop: () => {
                e(),
                n()
            }
        }
    }
    function X(t) {
        return `${t.name || "Error"}: ${t.message}`
    }
    function V(t) {
        return t.filter((t => null == t.url || !t.url.includes("sls-rum.js")))
    }
    function K(t) {
        let e = X(t);
        return t.stack.forEach((t => {
            const n = "?" === t.func ? "<anonymous>" : t.func
              , r = t.args && t.args.length > 0 ? `(${t.args.join(", ")})` : "";
            e += `\n  at ${n}${r} @ ${t.url}${t.line ? `:${t.line}` : ""}${t.line && t.column ? `:${t.column}` : ""}`
        }
        )),
        encodeURIComponent(e)
    }
    function J(t, e, n, r=!0) {
        var o;
        if (!t || void 0 === t.message && !(e instanceof Error))
            return {
                message: `${n} ${JSON.stringify(e)}`,
                stacktrace: "",
                type: t && t.name,
                id: y()
            };
        (null == t ? void 0 : t.stack) && r && (t.stack = V(t.stack));
        const i = null == (o = null == t ? void 0 : t.stack) ? void 0 : o[0];
        return {
            message: encodeURIComponent(t.message || "Empty message"),
            stacktrace: K(t),
            type: t.name,
            col: i ? i.column : void 0,
            line: i ? i.line : void 0,
            file: encodeURIComponent(i && i.url ? i.url : ""),
            id: y()
        }
    }
    function Y() {
        const t = new Error;
        let e;
        return o(( () => {
            const n = $(t);
            (null == n ? void 0 : n.stack) && (n.stack = V(n.stack)),
            e = K(n)
        }
        )),
        e
    }
    const Q = 8
      , Z = 16
      , tt = "b3"
      , et = "traceparent"
      , nt = "uber-trace-id"
      , rt = "X-B3-TraceId"
      , ot = "X-B3-SpanId"
      , it = Array(32);
    function st(t) {
        for (let e = 0; e < 2 * t; e++)
            it[e] = Math.floor(16 * Math.random()) + 48,
            it[e] >= 58 && (it[e] += 39);
        return String.fromCharCode.apply(null, it.slice(0, 2 * t))
    }
    function at() {
        return st(Z)
    }
    function ct() {
        return st(Q)
    }
    function ut(t, e) {
        return `${t}-${e}-1`
    }
    function lt(t, e) {
        return `00-${t}-${e}-01`
    }
    function pt(t, e) {
        return `${t}:${e}:0:1`
    }
    const ft = {
        b3: {
            name: tt,
            getter: ut
        },
        traceparent: {
            name: et,
            getter: lt
        },
        uber: {
            name: nt,
            getter: pt
        }
    };
    function dt(t, e, n) {
        null != t && Object.keys(t).map((r => {
            null == n || "" == n ? e[r] = t[r] : e[`${n}.${r}`] = t[r]
        }
        ))
    }
    const ht = "SLS_CLIENT";
    var mt = (t => (t.ERROR = "error",
    t.LOG = "log",
    t.LOCATION = "pv",
    t.API = "api",
    t.RESOURCE = "res",
    t.RESOURCE_ERROR = "res_err",
    t.PERF = "perf",
    t.CONSOLE_LOG = "console",
    t.DOM_CLICK = "dom_click",
    t))(mt || {})
      , bt = (t => (t.LOG_SEND = "LOG_SEND",
    t.BROWSER_SEND = "BROWSER_SEND",
    t.BASE_TRANSFORM = "BASE_TRANSFORM",
    t.BROWSER_BASE_TRANSFORM = "BROWSER_BASE_TRANSFORM",
    t.BROWSER_FETCH = "BROWSER_FETCH",
    t.BROWSER_XHR = "BROWSER_XHR",
    t.BROWSER_DOM = "BROWSER_DOM",
    t.BROWSER_LOCATION = "BROWSER_LOCATION",
    t.BROWSER_RUNTIME_ERROR = "BROWSER_RUNTIME_ERROR",
    t.BROWSER_CUSTOM_ERROR = "BROWSER_CUSTOM_ERROR",
    t.BROWSER_RESOURCE_ERROR = "BROWSER_RESOURCE_ERROR",
    t.BROWSER_CONSOLE = "BROWSER_CONSOLE",
    t.BROWSER_PERF = "BROWSER_PERF",
    t.BROWSER_RESOURSE = "BROWSER_RESOURSE",
    t.MINI_SEND = "MINI_SEND",
    t.MINI_REQUEST = "MINI_REQUEST",
    t.MINI_BASE_TRANSFORM = "MINI_BASE_TRANSFORM",
    t.MINI_ROUTE = "MINI_ROUTE",
    t))(bt || {});
    const gt = {
        BROWSER_SEND: -1,
        MINI_SEND: -2,
        BASE_TRANSFORM: 100,
        BROWSER_BASE_TRANSFORM: 200,
        MINI_BASE_TRANSFORM: 201,
        BROWSER_PERF: 301,
        BROWSER_FETCH: 400,
        BROWSER_XHR: 401,
        MINI_REQUEST: 402,
        BROWSER_RUNTIME_ERROR: 500
    }
      , Ot = "sls-trace-uid";
    var Rt = (t => (t.OK = "OK",
    t.ERROR = "ERROR",
    t.UNSET = "UNSET",
    t))(Rt || {})
      , yt = Object.defineProperty
      , Et = Object.defineProperties
      , vt = Object.getOwnPropertyDescriptors
      , St = Object.getOwnPropertySymbols
      , wt = Object.prototype.hasOwnProperty
      , Tt = Object.prototype.propertyIsEnumerable
      , _t = (t, e, n) => e in t ? yt(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , It = (t, e) => {
        for (var n in e || (e = {}))
            wt.call(e, n) && _t(t, n, e[n]);
        if (St)
            for (var n of St(e))
                Tt.call(e, n) && _t(t, n, e[n]);
        return t
    }
      , Pt = (t, e) => Et(t, vt(e));
    function xt(t, e, n) {
        if (e < 0)
            return;
        const r = n => {
            xt(t, e - 1, n)
        }
          , o = t[e];
        E(( () => {
            o.callback.call(void 0, n, r)
        }
        ), "plugin notify run error")()
    }
    class Bt {
        constructor(t) {
            this.subscribeMap = {},
            this.allNotifiers = [],
            this.allNotifiers = t
        }
        subscribeOne(t, e, n, r) {
            var o;
            const i = null != (o = this.subscribeMap[e]) ? o : [];
            this.subscribeMap[e] = i,
            i.push({
                name: t,
                priority: r,
                callback: n
            }),
            i.sort(( (t, e) => t.priority - e.priority))
        }
        notify(t, e) {
            var n;
            const r = null != (n = this.subscribeMap[t]) ? n : [];
            xt(r, r.length - 1, e)
        }
        subscribe(t, e, n, r) {
            if ("*" === e)
                for (let o = 0; o < this.allNotifiers.length; o++) {
                    const e = this.allNotifiers[o];
                    t !== e && this.subscribeOne(t, e, n, r)
                }
            else
                this.subscribeOne(t, e, n, r)
        }
        getSubscribeMap() {
            return this.subscribeMap
        }
    }
    var Ct = Object.defineProperty
      , Lt = Object.defineProperties
      , Nt = Object.getOwnPropertyDescriptors
      , kt = Object.getOwnPropertySymbols
      , jt = Object.prototype.hasOwnProperty
      , At = Object.prototype.propertyIsEnumerable
      , Mt = (t, e, n) => e in t ? Ct(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n;
    const $t = ["uid", "nickname", "env", "service", "version", "custom", "namespace"];
    class Ut {
        constructor(t) {
            var e, n;
            this.isInit = !1,
            this.pendingPlugins = [],
            this.pluginMap = {},
            this.session = function() {
                const t = at();
                let e = ct();
                return {
                    getSessionId: () => t,
                    getPageId: () => e,
                    refreshPageId: () => {
                        e = ct()
                    }
                }
            }(),
            this.options = t,
            this.use({
                name: bt.LOG_SEND,
                run: function() {}
            }),
            this.use({
                name: bt.BASE_TRANSFORM,
                run: function() {
                    this.subscribe("*", ( (t, e) => {
                        var n, r;
                        const {otBase: o, extra: i} = t;
                        o.service = this.options.service,
                        o.attribute = Pt(It(It({}, null != (n = this.options.attribute) ? n : {}), o.attribute), {
                            sid: this.session.getSessionId(),
                            pid: this.session.getPageId(),
                            uid: this.options.uid
                        }),
                        this.options.nickname && (o.attribute.nickname = this.options.nickname),
                        dt(this.options.custom, o.attribute, "custom"),
                        o.resource = It(It({}, null != (r = this.options.resource) ? r : {}), o.resource),
                        dt({
                            "uem.sdk.version": m,
                            workspace: this.options.workspace,
                            "deployment.environment": this.options.env
                        }, o.resource),
                        this.options.namespace && (o.resource["service.namespace"] = this.options.namespace),
                        this.options.version && (o.resource["service.version"] = this.options.version),
                        e({
                            otBase: o,
                            extra: i
                        })
                    }
                    ), gt[bt.BASE_TRANSFORM])
                }
            }),
            this.options.env = null != (e = t.env) ? e : "prod",
            this.options.version = null != (n = t.version) ? n : "-"
        }
        initPlugin(t) {
            if (null == t || "object" != typeof t)
                return void console.error("plugin is not a object");
            if (null == t.name || "" === t.name)
                return void console.error("plugin name is required.");
            if (this.pluginMap[t.name])
                return void console.error(`plugin name: ${t.name} is conflict`);
            if ("function" != typeof t.run)
                return void console.error("plugin.run is not a function");
            const e = (n = ( (t, e) => {
                for (var n in e || (e = {}))
                    jt.call(e, n) && Mt(t, n, e[n]);
                if (kt)
                    for (var n of kt(e))
                        At.call(e, n) && Mt(t, n, e[n]);
                return t
            }
            )({}, this.context),
            Lt(n, Nt({
                subscribe: (e, n, r) => {
                    this.sub.subscribe(t.name, e, n, r)
                }
                ,
                notify: e => {
                    this.sub.notify(t.name, e)
                }
            })));
            var n;
            E(( () => t.run.call(e)), `plugin ${t.name} init failed`)()
        }
        addLog(t) {
            if (this.isInit) {
                const e = {
                    t: mt.LOG
                };
                dt(t, e, mt.LOG);
                const n = {
                    start: 1e3 * L(),
                    attribute: e,
                    resource: {}
                };
                this.sub.notify(bt.LOG_SEND, {
                    otBase: n,
                    extra: {}
                })
            } else
                console.error("log should call after start")
        }
        setOptions(t) {
            this.isInit ? $t.forEach((e => {
                t[e] !== this.options[e] && null != t[e] && "" != t[e] && (this.options[e] = t[e],
                "uid" === e && "function" == typeof this.setLocalStorage && this.setLocalStorage(Ot, t[e]))
            }
            )) : console.error("setOptions should call after start")
        }
        start() {
            if (!this.isInit) {
                this.isInit = !0;
                let t = this.options.uid;
                null != t && "" !== t || ("function" == typeof this.getLocalStorage && (t = this.getLocalStorage(Ot)),
                null != t && "" !== t || (t = function(t=20) {
                    var e, n;
                    const r = new Array(t)
                      , o = Date.now().toString(36).split("");
                    for (; t-- > 0; )
                        n = (e = 36 * Math.random() | 0).toString(36),
                        r[t] = e % 3 ? n : n.toUpperCase();
                    for (var i = 0; i < 8; i++)
                        r.splice(3 * i + 2, 0, o[i]);
                    return r.join("")
                }())),
                this.options.uid = t,
                "function" == typeof this.setLocalStorage && this.setLocalStorage(Ot, t);
                const e = this.pendingPlugins.map((t => null == t ? void 0 : t.name)).filter((t => null != t));
                this.sub = new Bt(e),
                this.context = {
                    options: this.options,
                    session: this.session
                };
                for (const n of this.pendingPlugins)
                    this.initPlugin(n)
            }
        }
        use(t) {
            this.isInit ? console.error(`plugin: ${null == t ? void 0 : t.name} use should run before start`) : this.pendingPlugins.push(t)
        }
    }
    var Dt = Object.defineProperty
      , Wt = Object.getOwnPropertySymbols
      , Ht = Object.prototype.hasOwnProperty
      , Ft = Object.prototype.propertyIsEnumerable
      , qt = (t, e, n) => e in t ? Dt(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , zt = (t, e) => {
        for (var n in e || (e = {}))
            Ht.call(e, n) && qt(t, n, e[n]);
        if (Wt)
            for (var n of Wt(e))
                Ft.call(e, n) && qt(t, n, e[n]);
        return t
    }
    ;
    class Gt {
        constructor() {
            this.dep = new Map
        }
        subscribe(t, e) {
            const n = this.dep.get(t);
            this.dep.set(t, n ? n.concat(e) : [e])
        }
        notify(t, e) {
            const n = this.dep.get(t);
            t && n && n.forEach((t => {
                try {
                    t(e)
                } catch (n) {
                    console.error(n)
                }
            }
            ))
        }
    }
    function Xt() {
        return {
            name: bt.BROWSER_RUNTIME_ERROR,
            run: function() {
                const t = this;
                G(( (e, n) => {
                    const r = J(e, n, "Uncaught");
                    if (_(decodeURIComponent(r.message), t.options.ignoreRuntimeErrorConfig))
                        return;
                    const o = function(t) {
                        const e = {
                            t: mt.ERROR
                        }
                          , n = {
                            start: 1e3 * L(),
                            attribute: e,
                            resource: {}
                        };
                        return dt(t, e, "ex"),
                        {
                            otBase: n,
                            extra: {}
                        }
                    }(r);
                    t.notify(o)
                }
                ))
            }
        }
    }
    function Vt() {
        return {
            name: bt.BROWSER_CUSTOM_ERROR,
            run: function() {
                this.subscribe(bt.BROWSER_CUSTOM_ERROR, ( (t, e) => {
                    const {extra: n} = t
                      , r = null == n ? void 0 : n.ex;
                    if ("[object Error]" === Object.prototype.toString.call(r)) {
                        const t = function(t) {
                            const e = {
                                t: mt.ERROR
                            }
                              , n = {
                                start: 1e3 * L(),
                                attribute: e,
                                resource: {}
                            };
                            return dt(t, e, "ex"),
                            {
                                otBase: n,
                                extra: {}
                            }
                        }(J($(r), r.message, "Uncaught"));
                        e(t)
                    }
                }
                ), gt[bt.BROWSER_CUSTOM_ERROR])
            }
        }
    }
    var Kt = (t => (t.BEFORE_UNLOAD = "beforeunload",
    t.CLICK = "click",
    t.DBL_CLICK = "dblclick",
    t.KEY_DOWN = "keydown",
    t.LOAD = "load",
    t.POP_STATE = "popstate",
    t.SCROLL = "scroll",
    t.TOUCH_START = "touchstart",
    t.TOUCH_END = "touchend",
    t.TOUCH_MOVE = "touchmove",
    t.VISIBILITY_CHANGE = "visibilitychange",
    t.DOM_CONTENT_LOADED = "DOMContentLoaded",
    t.POINTER_DOWN = "pointerdown",
    t.POINTER_UP = "pointerup",
    t.POINTER_CANCEL = "pointercancel",
    t.HASH_CHANGE = "hashchange",
    t.PAGE_HIDE = "pagehide",
    t.MOUSE_DOWN = "mousedown",
    t.MOUSE_UP = "mouseup",
    t.MOUSE_MOVE = "mousemove",
    t.FOCUS = "focus",
    t.BLUR = "blur",
    t.CONTEXT_MENU = "contextmenu",
    t.RESIZE = "resize",
    t.CHANGE = "change",
    t.INPUT = "input",
    t.PLAY = "play",
    t.PAUSE = "pause",
    t.ERROE = "error",
    t))(Kt || {});
    function Jt(t, e, n, r) {
        return Yt(t, [e], n, r)
    }
    function Yt(t, e, n, {once: r, capture: o, passive: s}={}) {
        const a = i(r ? t => {
            u(),
            n(t)
        }
        : n)
          , c = s ? {
            capture: o,
            passive: s
        } : o;
        e.forEach((e => t.addEventListener(e, a, c)));
        const u = () => e.forEach((e => t.removeEventListener(e, a, c)));
        return {
            stop: u
        }
    }
    function Qt(t, e) {
        if (document.readyState === t || "complete" === document.readyState)
            e();
        else {
            Jt(window, "complete" === t ? "load" : "DOMContentLoaded", e, {
                once: !0
            })
        }
    }
    /*! lil-uri - v0.3.1 - MIT License - https://github.com/lil-js/uri */
    function Zt(t, e, n) {
        const r = [];
        return t && r.push(t),
        e && r.push(e),
        n && (t || r.push("/"),
        r.push("#" + n)),
        r.join("")
    }
    function te(t) {
        return ee(t, function(t) {
            if (t.origin)
                return t.origin;
            const e = t.host.replace(/(:80|:443)$/, "");
            return `${t.protocol}//${e}`
        }(window.location)).href
    }
    function ee(t, e) {
        if (function() {
            if (void 0 !== ne)
                return ne;
            try {
                const t = new URL("http://test/path");
                return ne = "http://test/path" === t.href,
                ne
            } catch (t) {
                ne = !1
            }
            return ne
        }())
            return void 0 !== e ? new URL(t,e) : new URL(t);
        if (void 0 === e && !/:/.test(t))
            throw new Error(`Invalid URL: '${t}'`);
        let n = document;
        const r = n.createElement("a");
        if (void 0 !== e) {
            n = document.implementation.createHTMLDocument("");
            const t = n.createElement("base");
            t.href = e,
            n.head.appendChild(t),
            n.body.appendChild(r)
        }
        return r.href = t,
        r
    }
    let ne;
    var re = Object.defineProperty
      , oe = Object.defineProperties
      , ie = Object.getOwnPropertyDescriptors
      , se = Object.getOwnPropertySymbols
      , ae = Object.prototype.hasOwnProperty
      , ce = Object.prototype.propertyIsEnumerable
      , ue = (t, e, n) => e in t ? re(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , le = (t, e) => {
        for (var n in e || (e = {}))
            ae.call(e, n) && ue(t, n, e[n]);
        if (se)
            for (var n of se(e))
                ce.call(e, n) && ue(t, n, e[n]);
        return t
    }
      , pe = (t, e) => oe(t, ie(e));
    const fe = "initial_document";
    function de() {
        return void 0 !== window.performance && "getEntries"in performance
    }
    function he(t) {
        return window.PerformanceObserver && void 0 !== PerformanceObserver.supportedEntryTypes && PerformanceObserver.supportedEntryTypes.includes(t)
    }
    function me(t, e) {
        var n;
        if (n = n => {
            Oe(t, e, n)
        }
        ,
        Qt("interactive", ( () => {
            let t;
            const e = {
                entryType: "resource",
                initiatorType: fe
            };
            if (he("navigation") && performance.getEntriesByType("navigation").length > 0) {
                const n = performance.getEntriesByType("navigation")[0];
                t = le(le({}, n.toJSON()), e)
            } else {
                const n = be();
                t = le(pe(le({}, n), {
                    decodedBodySize: 0,
                    duration: n.responseEnd,
                    name: window.location.href,
                    startTime: 0
                }), e)
            }
            n(t)
        }
        )),
        de() && ge(t, e, performance.getEntries()),
        window.PerformanceObserver) {
            const n = i((n => ge(t, e, n.getEntries())))
              , o = ["resource", "navigation", "longtask", "paint"]
              , s = ["largest-contentful-paint", "first-input", "layout-shift"];
            try {
                s.forEach((t => {
                    new PerformanceObserver(n).observe({
                        type: t,
                        buffered: !0
                    })
                }
                ))
            } catch (r) {
                o.push(...s)
            }
            new PerformanceObserver(n).observe({
                entryTypes: o
            }),
            de() && "addEventListener"in performance && performance.addEventListener("resourcetimingbufferfull", ( () => {
                performance.clearResourceTimings()
            }
            ))
        }
        he("navigation") || function(t) {
            function e() {
                t(pe(le({}, be()), {
                    entryType: "navigation"
                }))
            }
            Qt("complete", ( () => {
                setTimeout(i(e))
            }
            ))
        }((n => {
            Oe(t, e, n)
        }
        )),
        he("first-input") || function(t) {
            const e = Date.now();
            let n = !1;
            const {stop: r} = Yt(window, [Kt.CLICK, Kt.MOUSE_DOWN, Kt.KEY_DOWN, Kt.TOUCH_START, Kt.POINTER_DOWN], (t => {
                if (!t.cancelable)
                    return;
                const e = {
                    entryType: "first-input",
                    processingStart: N(),
                    startTime: t.timeStamp
                };
                t.type === Kt.POINTER_DOWN ? o(e) : i(e)
            }
            ), {
                passive: !0,
                capture: !0
            });
            function o(t) {
                Yt(window, [Kt.POINTER_UP, Kt.POINTER_CANCEL], (e => {
                    e.type === Kt.POINTER_UP && i(t)
                }
                ), {
                    once: !0
                })
            }
            function i(o) {
                if (!n) {
                    n = !0,
                    r();
                    const i = o.processingStart - o.startTime;
                    i >= 0 && i < Date.now() - e && t(o)
                }
            }
        }((n => {
            Oe(t, e, n)
        }
        ))
    }
    function be() {
        const t = {}
          , e = performance.timing;
        for (const n in e)
            if (b(e[n])) {
                const r = e[n];
                t[n] = 0 === r ? 0 : r - A()
            }
        return t
    }
    function ge(t, e, n) {
        n.forEach((n => {
            "resource" !== n.entryType && "navigation" !== n.entryType && "paint" !== n.entryType && "largest-contentful-paint" !== n.entryType && "first-input" !== n.entryType && "first-paint" !== n.entryType && "first-contentful-paint" !== n.entryType || Oe(t, e, n)
        }
        ))
    }
    function Oe(t, e, n) {
        (function(t) {
            return "navigation" === t.entryType && t.loadEventEnd <= 0
        }
        )(n) || t.notify(Te, n)
    }
    var Re = Object.defineProperty
      , ye = Object.getOwnPropertySymbols
      , Ee = Object.prototype.hasOwnProperty
      , ve = Object.prototype.propertyIsEnumerable
      , Se = (t, e, n) => e in t ? Re(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , we = (t, e) => {
        for (var n in e || (e = {}))
            Ee.call(e, n) && Se(t, n, e[n]);
        if (ye)
            for (var n of ye(e))
                ve.call(e, n) && Se(t, n, e[n]);
        return t
    }
    ;
    const Te = "PERFORMANCE_ENTRY_COLLECTED";
    function _e(t) {
        return t.fetchStart !== t.startTime
    }
    function Ie(...t) {
        for (let e = 1; e < t.length; e += 1)
            if (t[e - 1] > t[e])
                return !1;
        return !0
    }
    function Pe(t) {
        if (!Ie(t.startTime, t.fetchStart, t.domainLookupStart, t.domainLookupEnd, t.connectStart, t.connectEnd, t.requestStart, t.responseStart, t.responseEnd))
            return;
        if (!_e(t))
            return t;
        let {startTime: e, fetchStart: n, redirectStart: r, redirectEnd: o, domainLookupStart: i, domainLookupEnd: s, connectStart: a, secureConnectionStart: c, connectEnd: u, requestStart: l, responseStart: p, responseEnd: f} = t;
        return r < t.startTime && (r = t.startTime),
        o < t.startTime && (o = t.fetchStart),
        Ie(t.startTime, r, o, t.fetchStart) ? {
            startTime: e,
            fetchStart: n,
            redirectStart: r,
            redirectEnd: o,
            domainLookupStart: i,
            domainLookupEnd: s,
            connectStart: a,
            secureConnectionStart: c,
            connectEnd: u,
            requestStart: l,
            responseStart: p,
            responseEnd: f
        } : void 0
    }
    function xe(t) {
        const {duration: e, startTime: n, responseEnd: r} = t;
        return 0 === e && n < r ? C(k(n, r)) / 1e3 : C(e) / 1e3
    }
    function Be(t, e, n) {
        return [C(k(t, e)) / 1e3, C(k(e, n)) / 1e3]
    }
    function Ce(t) {
        const e = Pe(t);
        if (!e)
            return {};
        const {startTime: n, fetchStart: r, redirectStart: o, redirectEnd: i, domainLookupStart: s, domainLookupEnd: a, connectStart: c, secureConnectionStart: u, connectEnd: l, requestStart: p, responseStart: f, responseEnd: d} = e
          , h = {
            trans: Be(n, f, d),
            ttfb: Be(n, p, f)
        };
        return l !== r && (h.tcp = Be(n, c, l),
        Ie(c, u, l) && (h.ssl = Be(n, u, l))),
        a !== r && (h.dns = Be(n, s, a)),
        _e(t) && (h.red = Be(n, o, i)),
        h
    }
    function Le(t) {
        if (t.startTime < t.responseStart)
            return t.decodedBodySize
    }
    const Ne = [["document", t => fe === t], ["xhr", t => "xmlhttprequest" === t], ["fetch", t => "fetch" === t], ["beacon", t => "beacon" === t], ["css", (t, e) => /\.css$/i.test(e)], ["js", (t, e) => /\.js$/i.test(e)], ["image", (t, e) => O(["image", "img", "icon"], t) || null !== /\.(gif|jpg|jpeg|tiff|png|svg|ico)$/i.exec(e)], ["font", (t, e) => null !== /\.(woff|eot|woff2|ttf)$/i.exec(e)], ["media", (t, e) => O(["audio", "video"], t) || null !== /\.(mp3|mp4)$/i.exec(e)]];
    function ke(t, e) {
        if (!function(t) {
            try {
                return !!ee(t)
            } catch (e) {
                return !1
            }
        }(t))
            return "other";
        const n = function(t) {
            const e = ee(t).pathname;
            return "/" === e[0] ? e : `/${e}`
        }(t);
        for (const [r,o] of Ne)
            if (o(e, n))
                return r;
        return "other"
    }
    function je(t) {
        return we({
            duration: xe(t),
            size: Le(t)
        }, Ce(t))
    }
    const Ae = ["error", "warn", "log", "info", "debug"];
    let Me, $e;
    function Ue(t) {
        return Me || (Me = function(t) {
            const e = new r(( () => {
                var n;
                let r = null != (n = t.enableConsoleLog) && n;
                if (!window.console || !1 === r)
                    return;
                Ae.includes(r) || (r = "error");
                const o = Ae.slice(0, Ae.indexOf(r) + 1).map((t => {
                    const {stop: n} = q(console, t, {
                        after: (...n) => {
                            const r = {
                                message: [...n].map((t => function(t) {
                                    if ("string" == typeof t)
                                        return t;
                                    if (t instanceof Error)
                                        return X($(t));
                                    return JSON.stringify(t, void 0, 2)
                                }(t))).join(" "),
                                level: t,
                                stack: Y()
                            };
                            e.notify(r)
                        }
                    });
                    return n
                }
                ));
                return () => {
                    o.forEach((t => t()))
                }
            }
            ));
            return e
        }(t)),
        Me
    }
    function De(t=window) {
        return $e || ("hidden" === document.visibilityState ? $e = {
            timeStamp: 0
        } : ($e = {
            timeStamp: 1 / 0
        },
        Jt(t, Kt.PAGE_HIDE, ( ({timeStamp: t}) => {
            $e.timeStamp = t
        }
        ), {
            capture: !0,
            once: !0
        }))),
        $e
    }
    var We = Object.defineProperty
      , He = Object.getOwnPropertySymbols
      , Fe = Object.prototype.hasOwnProperty
      , qe = Object.prototype.propertyIsEnumerable
      , ze = (t, e, n) => e in t ? We(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , Ge = (t, e) => {
        for (var n in e || (e = {}))
            Fe.call(e, n) && ze(t, n, e[n]);
        if (He)
            for (var n of He(e))
                qe.call(e, n) && ze(t, n, e[n]);
        return t
    }
    ;
    const Xe = 6e5;
    function Ve(t) {
        return b(t) ? g(1e3 * t, 0) : t
    }
    function Ke(t, e) {
        let n, r = !1, o = 0;
        function i() {
            if (!1 === r) {
                r = !0;
                const t = {
                    t: mt.PERF
                };
                dt(n, t, mt.PERF);
                const o = {
                    start: 1e3 * L(),
                    attribute: t,
                    resource: {}
                };
                e.notify({
                    otBase: o,
                    extra: {}
                })
            }
        }
        function s(t, e) {
            n = Ge(Ge({}, n), t),
            e && (o = e),
            n.fit && 0 !== o && i()
        }
        setTimeout(( () => {
            i()
        }
        ), Xe),
        function(t, e) {
            t.subscribe(Te, (t => {
                if ("navigation" === t.entryType) {
                    const n = Ge({}, Ce(t));
                    0 != t.domContentLoadedEventEnd && (n.dcl = Ve(t.domContentLoadedEventEnd)),
                    t.domInteractive != t.fetchStart && (n.di = Ve(t.domInteractive - t.fetchStart)),
                    t.loadEventStart != t.fetchStart && (n.load = Ve(t.loadEventStart - t.fetchStart)),
                    t.responseEnd != t.domInteractive && (n.dom = Be(t.startTime, t.responseEnd, t.domInteractive)),
                    t.domContentLoadedEventEnd != t.loadEventStart && (n.res = Be(t.startTime, t.domContentLoadedEventEnd, t.loadEventStart)),
                    e(n, x(t.startTime).timeStamp)
                }
            }
            )),
            stop
        }(t, s),
        function(t, e) {
            const n = De();
            t.subscribe(Te, (t => {
                "paint" === t.entryType && "first-contentful-paint" === t.name && t.startTime < n.timeStamp && t.startTime < Xe && e(Ve(t.startTime))
            }
            ))
        }(t, (t => s({
            fcp: t
        }))),
        function(t, e) {
            const n = De();
            t.subscribe(Te, (t => {
                "largest-contentful-paint" === t.entryType && t.startTime < n.timeStamp && t.startTime < Xe && e(Ve(t.startTime))
            }
            ))
        }(t, (t => {
            s({
                lcp: t
            })
        }
        )),
        function(t, e) {
            const n = De();
            t.subscribe(Te, (t => {
                if ("first-input" === t.entryType && t.startTime < n.timeStamp) {
                    const n = k(t.startTime, t.processingStart);
                    e({
                        firstInputDelay: Ve(n >= 0 ? n : 0),
                        firstInputTime: Ve(t.startTime)
                    })
                }
            }
            ))
        }(t, ( ({firstInputDelay: t, firstInputTime: e}) => {
            s({
                fid: t,
                fit: e
            })
        }
        )),
        function(t, e) {
            const n = De();
            t.subscribe(Te, (t => {
                "paint" === t.entryType && "first-paint" === t.name && t.startTime < n.timeStamp && t.startTime < Xe && e(Ve(t.startTime))
            }
            ))
        }(t, (t => {
            s({
                fp: t
            })
        }
        ))
    }
    function Je(t) {
        if (!performance || !("getEntriesByName"in performance))
            return;
        const {extra: e} = t
          , n = performance.getEntriesByName(e.httpInfo.url, "resource");
        if (!n.length || !("toJSON"in n[0]))
            return;
        const r = n.map((t => t.toJSON())).filter(Pe).filter((t => function(t, e, n) {
            const r = 1;
            return t.startTime >= e - r && Ye(t) <= n + r
        }(t, e.relativeTime, Ye({
            startTime: e.relativeTime,
            duration: e.duration
        }))));
        return 1 === r.length ? r[0] : 2 === r.length && Ye((o = r)[0]) <= o[1].startTime ? r[1] : void 0;
        var o
    }
    function Ye(t) {
        return t.startTime + t.duration
    }
    function Qe() {
        return {
            name: bt.BROWSER_PERF,
            run: function() {
                let t = this;
                function e(e) {
                    const n = ke((r = e).name, r.initiatorType);
                    var r;
                    if (v(e.name, t.options))
                        return null;
                    const o = je(e);
                    return {
                        start: x(e.startTime).timeStamp,
                        resourceBase: {
                            type: n,
                            url: e.name,
                            id: y()
                        },
                        perf: o
                    }
                }
                this.subscribe(bt.BROWSER_FETCH, ( (t, e) => {
                    e(Ze(t))
                }
                ), gt[bt.BROWSER_PERF]),
                this.subscribe(bt.BROWSER_XHR, ( (t, e) => {
                    e(Ze(t))
                }
                ), gt[bt.BROWSER_PERF]);
                const n = new Gt;
                (this.options.enablePerf || null == this.options.enablePerf) && Ke(n, this),
                (this.options.enableResourcePerf || null == this.options.enableResourcePerf) && n.subscribe(Te, (t => {
                    if ("resource" === t.entryType && ("xmlhttprequest" !== (n = t).initiatorType && "fetch" !== n.initiatorType)) {
                        if (_(t.name, this.options.ignoreResourceConfig))
                            return;
                        const n = e(t);
                        if (null != n) {
                            const t = {
                                t: mt.RESOURCE
                            }
                              , e = {
                                start: 1e3 * n.start,
                                attribute: t,
                                resource: {}
                            };
                            dt(n.resourceBase, t, "resource"),
                            n.perf && dt(n.perf, t, "perf"),
                            this.notify({
                                otBase: e,
                                extra: {}
                            })
                        }
                    }
                    var n
                }
                )),
                me(n, this.options)
            }
        }
    }
    function Ze(t) {
        const e = Je(t)
          , n = e ? je(e) : {}
          , {otBase: r} = t;
        return n.duration && (r.duration = n.duration,
        delete n.duration),
        dt(n, r.attribute, mt.PERF),
        {
            otBase: r,
            extra: t.extra
        }
    }
    class tn {
        constructor(t) {
            var e, n;
            this.timer = null,
            this.time = 10,
            this.count = 10,
            this.arr = [],
            this.time = null != (e = t.time) ? e : 10,
            this.count = null != (n = t.count) ? n : 10,
            this.url = t.host.startsWith("http://") || t.host.startsWith("https://") ? t.host + "/logstores/" + t.logstore + "/track" : "https://" + t.project + "." + t.host + "/logstores/" + t.logstore + "/track",
            this.opt = t,
            t.installUnloadHook && "function" == typeof t.installUnloadHook && t.installUnloadHook(( () => {
                this.sendImmediateInner()
            }
            ))
        }
        assemblePayload(t) {
            const e = {
                __logs__: t
            };
            return this.opt.tags && (e.__tags__ = this.opt.tags),
            this.opt.topic && (e.__topic__ = this.opt.topic),
            this.opt.source && (e.__source__ = this.opt.source),
            JSON.stringify(e)
        }
        platformSend() {
            if (this.opt.sendPayload && "function" == typeof this.opt.sendPayload) {
                const t = this.assemblePayload(this.arr);
                this.opt.sendPayload(this.url, t)
            }
        }
        transString(t) {
            let e = {};
            for (let n in t)
                e[n] = "object" == typeof t[n] ? JSON.stringify(t[n]) : String(t[n]);
            return e
        }
        sendImmediateInner() {
            this.arr && this.arr.length > 0 && (this.platformSend(),
            null != this.timer && (clearTimeout(this.timer),
            this.timer = null),
            this.arr = [])
        }
        sendInner() {
            if (this.timer)
                this.arr.length >= this.count && (clearTimeout(this.timer),
                this.timer = null,
                this.sendImmediateInner());
            else {
                const t = this;
                this.arr.length >= this.count || this.time <= 0 ? this.sendImmediateInner() : this.timer = setTimeout((function() {
                    t.sendImmediateInner()
                }
                ), 1e3 * this.time)
            }
        }
        send(t) {
            const e = this.transString(t);
            this.arr.push(e),
            this.sendInner()
        }
        sendImmediate(t) {
            const e = this.transString(t);
            this.arr.push(e),
            this.sendImmediateInner()
        }
        sendBatchLogs(t) {
            const e = t.map((t => this.transString(t)));
            this.arr.push(...e),
            this.sendInner()
        }
        sendBatchLogsImmediate(t) {
            const e = t.map((t => this.transString(t)));
            this.arr.push(...e),
            this.sendImmediateInner()
        }
        overwriteTransString(t) {
            this.transString = t.transString
        }
        getOpt() {
            return this.opt
        }
    }
    var en = (t, e, n) => new Promise(( (r, o) => {
        var i = t => {
            try {
                a(n.next(t))
            } catch (e) {
                o(e)
            }
        }
          , s = t => {
            try {
                a(n.throw(t))
            } catch (e) {
                o(e)
            }
        }
          , a = t => t.done ? r(t.value) : Promise.resolve(t.value).then(i, s);
        a((n = n.apply(t, e)).next())
    }
    ));
    function nn(t, e) {
        const n = new window.XMLHttpRequest;
        n.open("POST", `${t}?APIVersion=0.6.0`, !0),
        n.send(e)
    }
    function rn(t, e) {
        try {
            if (e.length >= 32768)
                return void nn(t, e);
            (function(t, e) {
                return !(!navigator || !navigator.sendBeacon) && navigator.sendBeacon(`${t}?APIVersion=0.6.0`, e)
            }
            )(t, e) || nn(t, e)
        } catch (n) {
            window && window.console && "function" == typeof window.console.error && (console.error("Failed to log to ali log service because of this exception:\n" + n),
            console.error("Failed log data:", t))
        }
    }
    class on extends tn {
        constructor(t) {
            super(Object.assign({}, t, {
                installUnloadHook: t => {
                    window.addEventListener("beforeunload", ( () => {
                        t()
                    }
                    ))
                }
                ,
                sendPayload: (t, e) => {
                    rn(t, e)
                }
            }))
        }
        useStsPlugin(t) {
            this.getOpt().sendPayload = (e, n) => {
                !function(t, e, n) {
                    en(this, null, (function*() {
                        try {
                            t = t.slice(0, -6);
                            const {data: r, header: o} = yield n.process(t, e)
                              , i = new window.XMLHttpRequest;
                            i.open("POST", t, !0);
                            for (let t in o)
                                i.setRequestHeader(t, o[t]);
                            i.send(r)
                        } catch (r) {
                            window && window.console && "function" == typeof window.console.error && (console.error("Failed to log to ali log service because of this exception:\n" + r),
                            console.error("Failed log data:", t))
                        }
                    }
                    ))
                }(e, n, t)
            }
            ,
            this.overwriteTransString(t)
        }
    }
    n(window, "SLS_Tracker", on);
    var sn = Object.defineProperty
      , an = Object.getOwnPropertySymbols
      , cn = Object.prototype.hasOwnProperty
      , un = Object.prototype.propertyIsEnumerable
      , ln = (t, e, n) => e in t ? sn(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , pn = (t, e) => {
        for (var n in e || (e = {}))
            cn.call(e, n) && ln(t, n, e[n]);
        if (an)
            for (var n of an(e))
                un.call(e, n) && ln(t, n, e[n]);
        return t
    }
    ;
    const fn = new RegExp(["(android|bb\\d+|meego).+mobile|avantgo|bada\\/|blackberry|blazer|", "compal|elaine|fennec|hiptop|iemobile|ip(hone|od|ad)|iris|kindle|lge |maemo|", "midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)", "\\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\\.(browser|link)|vodafone|", "wap|windows ce|xda|xiino"].join(""),"i")
      , dn = new RegExp(["1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\\-)|", "ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\\-m|r |s )|", "avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\\-(n|u)|c55\\/|capi|ccwa|cdm\\-|", "cell|chtm|cldc|cmd\\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\\-s|devi|dica|dmob|do(c|p)o|", "ds(12|\\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\\-|_)|", "g1 u|g560|gene|gf\\-5|g\\-mo|go(\\.w|od)|gr(ad|un)|haie|hcit|hd\\-(m|p|t)|hei\\-|", "hi(pt|ta)|hp( i|ip)|hs\\-c|ht(c(\\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\\-(20|go|ma)|", "i230|iac( |\\-|\\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|", "kddi|keji|kgt( |\\/)|klon|kpt |kwc\\-|kyo(c|k)|le(no|xi)|lg( g|\\/(k|l|u)|50|54|\\-[a-w])", "|libw|lynx|m1\\-w|m3ga|m50\\/|ma(te|ui|xo)|mc(01|21|ca)|m\\-cr|me(rc|ri)|mi(o8|oa|ts)|", "mmef|mo(01|02|bi|de|do|t(\\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|", "n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|", "op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\\-2|", "po(ck|rt|se)|prox|psio|pt\\-g|qa\\-a|qc(07|12|21|32|60|\\-[2-7]|i\\-)|qtek|r380|r600|", "raks|rim9|ro(ve|zo)|s55\\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\\-|oo|p\\-)|sdk\\/|", "se(c(\\-|0|1)|47|mc|nd|ri)|sgh\\-|shar|sie(\\-|m)|k\\-0|sl(45|id)|sm(al|ar|b3|it|t5)|", "so(ft|ny)|sp(01|h\\-|v\\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\\-|tdg\\-|", "tel(i|m)|tim\\-|t\\-mo|to(pl|sh)|ts(70|m\\-|m3|m5)|tx\\-9|up(\\.b|g1|si)|utst|v400|v750|", "veri|vi(rg|te)|vk(40|5[0-3]|\\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|", "w3c(\\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\\-|your|zeto|zte\\-"].join(""),"i")
      , hn = "Windows"
      , mn = "macOS"
      , bn = "iOS"
      , gn = "Android"
      , On = "WebOS"
      , Rn = "Linux"
      , yn = "Chrome OS";
    function En(t, e) {
        const n = e.match(t);
        return n && n.length > 0 && n[1] || ""
    }
    const vn = [{
        test: [/windows /i],
        describe(t) {
            const e = En(/Windows ((NT|XP)( \d\d?.\d)?)/i, t);
            return {
                name: hn,
                version: e
            }
        }
    }, {
        test: [/Macintosh(.*?) FxiOS(.*?)\//],
        describe(t) {
            const e = function(t, e) {
                const n = e.match(t);
                return n && n.length > 1 && n[2] || ""
            }(/(Version\/)(\d[\d.]+)/, t);
            return e ? {
                name: bn,
                version: e
            } : {
                name: bn
            }
        }
    }, {
        test: [/macintosh/i],
        describe(t) {
            const e = En(/mac os x (\d+(\.?_?\d+)+)/i, t).replace(/[_\s]/g, ".");
            return {
                name: mn,
                version: e
            }
        }
    }, {
        test: [/(ipod|iphone|ipad)/i],
        describe(t) {
            const e = En(/os (\d+([_\s]\d+)*) like mac os x/i, t).replace(/[_\s]/g, ".");
            return {
                name: bn,
                version: e
            }
        }
    }, {
        test(t) {
            const e = !t.test(/like android/i)
              , n = t.test(/android/i);
            return e && n
        },
        describe(t) {
            const e = En(/android[\s/-](\d+(\.\d+)*)/i, t);
            return {
                name: gn,
                version: e
            }
        }
    }, {
        test: [/(web|hpw)[o0]s/i],
        describe(t) {
            const e = En(/(?:web|hpw)[o0]s\/(\d+(\.\d+)*)/i, t);
            return e ? {
                name: On,
                version: e
            } : {
                name: On
            }
        }
    }, {
        test: [/linux/i],
        describe: () => ({
            name: Rn
        })
    }, {
        test: [/CrOS/],
        describe: () => ({
            name: yn
        })
    }]
      , Sn = [["HuaweiBrowser", /HuaweiBrowser\/([0-9\._]+)/], ["UCBrowser", /UCBrowser\/([0-9\._]+)/], ["firefox", /Firefox\/([0-9\.]+)(?:\s|$)/], ["opera", /Opera\/([0-9\.]+)(?:\s|$)/], ["opera", /OPR\/([0-9\.]+)(:?\s|$)$/], ["edge", /Edge\/([0-9\._]+)/], ["edge", /Edg\/([0-9\._]+)/], ["ie", /Trident\/7\.0.*rv\:([0-9\.]+)\).*Gecko$/], ["ie", /MSIE\s([0-9\.]+);.*Trident\/[4-7].0/], ["ie", /MSIE\s(7\.0)/], ["safari", /Version\/([0-9\._]+).*Safari/], ["chrome", /(?!Chrom.*OPR)Chrom(?:e|ium)\/([0-9\.]+)(:?\s|$)/], ["bb10", /BB10;\sTouch.*Version\/([0-9\.]+)/], ["android", /Android\s([0-9\.]+)/], ["ios", /Version\/([0-9\._]+).*Mobile.*Safari.*/], ["yandexbrowser", /YaBrowser\/([0-9\._]+)/], ["crios", /CriOS\/([0-9\.]+)(:?\s|$)/]]
      , wn = "-";
    class Tn {
        constructor(t) {
            this.userAgent = null != t ? t : navigator ? navigator.userAgent || navigator.vendor : ""
        }
        detect() {
            return pn(pn(pn({}, this.checkBrowser()), this.checkMobile()), this.checkOs())
        }
        checkBrowser() {
            const t = Sn.filter((t => t[1].test(this.userAgent))).map((t => {
                const e = t[1].exec(this.userAgent);
                return {
                    browser_name: String(t[0]),
                    browser_version: null != e ? String(e[1]) : wn
                }
            }
            )).shift();
            return t || {
                browser_name: wn,
                browser_version: wn
            }
        }
        test(t) {
            return t.test(this.userAgent)
        }
        checkMobile() {
            const t = this.userAgent.substr(0, 4);
            return {
                os_type: fn.test(this.userAgent) || dn.test(t) ? "mobile" : "pc"
            }
        }
        checkOs() {
            var t;
            const e = vn.find((t => "function" == typeof t.test ? t.test(this) : t.test instanceof Array ? t.test.some((t => this.test(t))) : void 0));
            if (e) {
                const n = e.describe(this.userAgent);
                return {
                    os: n.name,
                    os_version: null != (t = n.version) ? t : wn
                }
            }
            return {
                os: wn,
                os_version: wn
            }
        }
    }
    var _n = Object.defineProperty
      , In = Object.defineProperties
      , Pn = Object.getOwnPropertyDescriptors
      , xn = Object.getOwnPropertySymbols
      , Bn = Object.prototype.hasOwnProperty
      , Cn = Object.prototype.propertyIsEnumerable
      , Ln = (t, e, n) => e in t ? _n(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , Nn = (t, e) => {
        for (var n in e || (e = {}))
            Bn.call(e, n) && Ln(t, n, e[n]);
        if (xn)
            for (var n of xn(e))
                Cn.call(e, n) && Ln(t, n, e[n]);
        return t
    }
      , kn = (t, e) => In(t, Pn(e));
    function jn() {
        return {
            name: bt.BROWSER_BASE_TRANSFORM,
            run: function() {
                this.subscribe("*", ( (t, e) => {
                    const {otBase: n, extra: r} = t
                      , o = new Tn(i).detect();
                    var i;
                    n.resource = kn(Nn({}, n.resource), {
                        "browser.name": o.browser_name,
                        "browser.version": o.browser_version,
                        "browser.screen": `${window.innerWidth}x${window.innerHeight}`,
                        "device.screen": `${window.screen.width}x${window.screen.height}`,
                        "user_agent.original": navigator ? navigator.userAgent : "",
                        "os.type": o.os_type,
                        "os.version": o.os_version,
                        "os.name": o.os,
                        "uem.data.type": "web"
                    }),
                    function(t) {
                        const {pathname: e, search: n, hash: r} = window.location
                          , o = Zt(e, n, r)
                          , i = "" == document.referrer ? `${window.location.origin}/` : document.referrer;
                        dt({
                            host: encodeURIComponent(window.location.host),
                            target: encodeURIComponent(o),
                            referrer: encodeURIComponent(i),
                            target_original: o,
                            referrer_original: i
                        }, t, "page")
                    }(n.attribute);
                    const s = {
                        otBase: n,
                        extra: r
                    };
                    e(s)
                }
                ), gt[bt.BROWSER_BASE_TRANSFORM])
            }
        }
    }
    function An(t) {
        var e;
        const n = t.tagName.toLowerCase();
        let r = t.classList.value;
        r = "" !== r ? ` class="${r}"` : "";
        const o = t.id ? ` id="${t.id}"` : ""
          , i = t.innerText
          , s = null != (e = t.dataset) ? e : {}
          , a = Object.keys(t.dataset).map((t => `data-${t}="${s[t]}"`)).join(" ");
        return `<${n}${o}${"" !== r ? r : ""}${"" !== a ? ` ${a}` : ""}>${i}</${n}>`
    }
    function Mn() {
        return {
            name: bt.BROWSER_DOM,
            run: function() {
                const {clickThrottleTime: t=300} = this.options
                  , e = function(t, e) {
                    let n = !0;
                    return function(...r) {
                        n && (t.apply(this, r),
                        n = !1,
                        setTimeout(( () => {
                            n = !0
                        }
                        ), e))
                    }
                }(( (t, e) => {
                    const n = ((r = t.activeElement) ? "body" === r.tagName.toLowerCase() ? null : An(r) : null) || function(t, e) {
                        if (!t || !e)
                            return null;
                        const n = t.tagName.toLowerCase();
                        if (0 === e.length) {
                            if ("a" !== n)
                                return null
                        } else if (!e.some((t => {
                            if ("function" == typeof t)
                                try {
                                    return t(n)
                                } catch (e) {
                                    return console.error("user function callback threw an error:", e),
                                    !1
                                }
                            return "string" == typeof t && n === t
                        }
                        )))
                            return null;
                        return An(t)
                    }(e.target, this.options.monitoredDomType);
                    var r;
                    if (!n)
                        return null;
                    const o = {
                        t: mt.DOM_CLICK,
                        "dom.el": n
                    }
                      , i = {
                        otBase: {
                            start: 1e3 * L(),
                            attribute: o,
                            resource: {}
                        },
                        extra: {}
                    };
                    return this.notify(i),
                    null
                }
                ), t);
                document.addEventListener("click", (function(t) {
                    e(this, t)
                }
                ), !0)
            }
        }
    }
    var $n = (t, e, n) => new Promise(( (r, o) => {
        var i = t => {
            try {
                a(n.next(t))
            } catch (e) {
                o(e)
            }
        }
          , s = t => {
            try {
                a(n.throw(t))
            } catch (e) {
                o(e)
            }
        }
          , a = t => t.done ? r(t.value) : Promise.resolve(t.value).then(i, s);
        a((n = n.apply(t, e)).next())
    }
    ));
    let Un;
    function Dn(t) {
        return Un || (Un = function(t) {
            const e = new r(( () => {
                if (!window.fetch)
                    return;
                const {stop: n} = F(window, "fetch", (n => function(r, i) {
                    let s;
                    const a = te("object" == typeof r && r.url || r)
                      , c = ct()
                      , u = at();
                    t.enableTrace && (null == t.enableTraceRequestConfig && a.startsWith(window.location.origin) || null != t.enableTraceRequestConfig && I(a, t.enableTraceRequestConfig)) && (i = function(t, e, n, r, o, i="headers") {
                        var s;
                        const a = null != n ? n : {};
                        a[i] = null != (s = a[i]) ? s : {},
                        "Headers" === a[i].constructor.name ? (a[i].append(tt, ut(t, e)),
                        a[i].append(et, lt(t, e)),
                        a[i].append(nt, pt(t, e)),
                        o && a[i].append(rt, t),
                        o && a[i].append(ot, e)) : (a[i][tt] = ut(t, e),
                        a[i][et] = lt(t, e),
                        a[i][nt] = pt(t, e),
                        o && (a[i][rt] = t),
                        o && (a[i][ot] = e));
                        try {
                            if (r)
                                if (r instanceof Function) {
                                    const n = E(r, "run customTraceHeaders func error.")(t, e);
                                    if (n)
                                        for (const [t,e] of Object.entries(n))
                                            "Headers" === a[i].constructor.name ? a[i].append(t, e) : a[i][t] = e
                                } else
                                    for (const [n,o] of Object.entries(r))
                                        ft[o] && ("Headers" === a[i].constructor.name ? a[i].append(n, ft[o].getter(t, e)) : a[i][n] = ft[o].getter(t, e))
                        } catch (c) {
                            console.error("Failed utilizing customTraceHeaders.", c)
                        }
                        return a
                    }(u, c, i, t.customTraceHeaders, t.enableXb3));
                    const l = o(Wn, null, [r, a, u, c, i]);
                    return l ? (s = n.call(this, l.input, l.init),
                    o(Hn, null, [e, s, l])) : s = n.call(this, r, i),
                    s
                }
                ));
                return n
            }
            ));
            return e
        }(t)),
        Un
    }
    function Wn(t, e, n, r, o) {
        return {
            init: o,
            input: t,
            method: o && o.method || "object" == typeof t && t.method || "GET",
            start: L(),
            url: e,
            relativeTime: N(),
            spanID: r,
            traceID: n
        }
    }
    function Hn(t, e, n) {
        const r = e => $n(this, null, (function*() {
            const r = n;
            if (r.end = L(),
            r.duration = k(r.start, r.end),
            "stack"in e || e instanceof Error)
                r.status = 0,
                r.responseText = K($(e)),
                r.isAborted = e instanceof DOMException && e.code === DOMException.ABORT_ERR,
                r.error = e,
                t.notify(r);
            else if ("status"in e) {
                let n;
                try {
                    n = yield e.clone().text()
                } catch (o) {
                    n = `Unable to retrieve response: ${o}`
                }
                r.response = e,
                r.responseText = n,
                r.responseType = e.type,
                r.status = e.status,
                r.isAborted = !1,
                r.body = null != r.init && null != r.init.body ? r.init.body.toString() : void 0,
                t.notify(r)
            }
        }
        ));
        e.then(i(r), i(r))
    }
    var Fn = Object.defineProperty
      , qn = Object.getOwnPropertySymbols
      , zn = Object.prototype.hasOwnProperty
      , Gn = Object.prototype.propertyIsEnumerable
      , Xn = (t, e, n) => e in t ? Fn(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , Vn = (t, e) => {
        for (var n in e || (e = {}))
            zn.call(e, n) && Xn(t, n, e[n]);
        if (qn)
            for (var n of qn(e))
                Gn.call(e, n) && Xn(t, n, e[n]);
        return t
    }
    ;
    function Kn(t) {
        let e = Vn({}, t);
        const n = new r(( () => {
            const {stop: t} = function(t) {
                const {stop: e} = q(history, "pushState", {
                    after: t
                })
                  , {stop: n} = q(history, "replaceState", {
                    after: t
                })
                  , {stop: r} = Jt(window, Kt.POP_STATE, t);
                return {
                    stop: () => {
                        e(),
                        n(),
                        r()
                    }
                }
            }(o)
              , {stop: e} = Jt(window, Kt.HASH_CHANGE, o);
            return () => {
                t(),
                e()
            }
        }
        ));
        function o() {
            if (e.href === t.href)
                return;
            const r = Vn({}, t);
            n.notify({
                newLocation: r,
                oldLocation: e
            }),
            e = r
        }
        return n
    }
    function Jn(t, e, n) {
        const {pathname: r, search: o, hash: i} = t
          , s = Zt(r, o, i);
        dt({
            [`target_${e}`]: encodeURIComponent(s),
            [`target_${e}_original`]: s
        }, n, "page")
    }
    var Yn = Object.defineProperty
      , Qn = Object.getOwnPropertySymbols
      , Zn = Object.prototype.hasOwnProperty
      , tr = Object.prototype.propertyIsEnumerable
      , er = (t, e, n) => e in t ? Yn(t, e, {
        enumerable: !0,
        configurable: !0,
        writable: !0,
        value: n
    }) : t[e] = n
      , nr = (t, e) => {
        for (var n in e || (e = {}))
            Zn.call(e, n) && er(t, n, e[n]);
        if (Qn)
            for (var n of Qn(e))
                tr.call(e, n) && er(t, n, e[n]);
        return t
    }
    ;
    let rr;
    const or = new WeakMap;
    function ir(t) {
        return rr || (rr = function(t) {
            const e = new r(( () => {
                function n(e, n, r) {
                    const o = v(n, t);
                    or.set(this, {
                        method: e,
                        url: te(n),
                        isInternal: !!o
                    })
                }
                const {stop: r} = q(XMLHttpRequest.prototype, "open", {
                    before: n
                })
                  , {stop: o} = q(XMLHttpRequest.prototype, "send", {
                    before(n) {
                        sr.call(this, e, n, t)
                    }
                })
                  , {stop: i} = q(XMLHttpRequest.prototype, "abort", {
                    before: ar
                });
                return () => {
                    r(),
                    o(),
                    i()
                }
            }
            ));
            return e
        }(t)),
        rr
    }
    function sr(t, e, n) {
        const r = or.get(this);
        if (!r)
            return;
        const o = ct()
          , s = at()
          , a = r;
        a.start = L(),
        a.relativeTime = N(),
        a.isAborted = !1,
        a.xhr = this,
        a.spanID = o,
        a.traceID = s,
        a.body = e;
        const c = r.url;
        n.enableTrace && (null == n.enableTraceRequestConfig && c.startsWith(window.location.origin) || null != n.enableTraceRequestConfig && I(c, n.enableTraceRequestConfig)) && function(t, e, n, r, o) {
            t.setRequestHeader(tt, ut(e, n)),
            t.setRequestHeader(et, lt(e, n)),
            t.setRequestHeader(nt, pt(e, n)),
            o && t.setRequestHeader(rt, e),
            o && t.setRequestHeader(ot, n);
            try {
                if (r)
                    if (r instanceof Function) {
                        const o = E(r, "run customTraceHeaders func error.")(e, n);
                        if (o)
                            for (const [e,n] of Object.entries(o))
                                t.setRequestHeader(e, n)
                    } else
                        for (const [o,i] of Object.entries(r))
                            ft[i] && t.setRequestHeader(o, ft[i].getter(e, n))
            } catch (i) {
                console.error("Failed utilizing customTraceHeaders.", i)
            }
        }(this, s, o, n.customTraceHeaders, n.enableXb3);
        let u = !1;
        const {stop: l} = q(this, "onreadystatechange", {
            before() {
                this.readyState === XMLHttpRequest.DONE && p()
            }
        })
          , p = i(( () => {
            if (this.removeEventListener("loadend", p),
            l(),
            u)
                return;
            u = !0;
            const e = r;
            e.end = L(),
            e.duration = k(a.start, e.end),
            e.responseText = this.response,
            e.status = this.status,
            t.notify(nr({}, e))
        }
        ));
        this.addEventListener("loadend", p)
    }
    function ar() {
        const t = or.get(this);
        t && (t.isAborted = !0)
    }
    class cr extends Ut {
        constructor(t) {
            var e;
            super(t),
            this.options.service = null != (e = t.service) ? e : "web"
        }
        setLocalStorage(t, e) {
            window.localStorage.setItem(t, e)
        }
        getLocalStorage(t) {
            return window.localStorage.getItem(t)
        }
        addError(t) {
            this.isInit ? this.sub.notify(bt.BROWSER_CUSTOM_ERROR, {
                otBase: {},
                extra: {
                    ex: t
                }
            }) : console.error("addError should call after start")
        }
    }
    const ur = function(t, e) {
        var n;
        const r = {
            current: void 0
        }
          , o = [];
        let i = {};
        return "function" == typeof e && (i = null != (n = e(r)) ? n : {}),
        zt({
            init: e => {
                if (null != r.current)
                    return;
                r.current = t(e);
                const n = r.current;
                o.forEach((t => {
                    n.use(t)
                }
                )),
                n.start()
            }
            ,
            use: t => {
                o.push(t)
            }
            ,
            addLog: t => {
                const e = r.current;
                e && e.addLog(t)
            }
            ,
            onReady(t) {
                t()
            },
            setOptions: t => {
                const e = r.current;
                e && e.setOptions(t)
            }
        }, i)
    }((t => {
        const e = new cr(t);
        var n;
        return R(t.enableRequest, !0) && e.use({
            name: bt.BROWSER_FETCH,
            run: function() {
                Dn(this.options).subscribe((t => {
                    var e, n;
                    const r = t.status >= 200 && t.status < 400;
                    if (_(t.url, this.options.ignoreRequestConfig, t.status))
                        return;
                    const o = w(t.url)
                      , i = {
                        start: 1e3 * t.start,
                        end: 1e3 * t.end,
                        duration: 1e3 * t.duration,
                        host: "",
                        kind: "client",
                        links: [],
                        logs: [],
                        name: `${t.method} ${null != o ? o.path : t.input}`,
                        parentSpanID: "",
                        spanID: t.spanID,
                        statusCode: r ? Rt.OK : Rt.ERROR,
                        statusMessage: null != (n = null == (e = t.response) ? void 0 : e.statusText) ? n : "",
                        traceID: t.traceID,
                        attribute: {
                            t: mt.API
                        },
                        resource: {}
                    }
                      , s = T(t.url, t.method, t.status, o);
                    dt(s, i.attribute, "http");
                    const a = {
                        otBase: i,
                        extra: {
                            start: t.start,
                            relativeTime: t.relativeTime,
                            duration: t.duration,
                            httpInfo: s,
                            httpContext: t
                        }
                    };
                    P(this.options.enableRequestBodyConfig, a, r) && (i.attribute["http.request.body"] = t.body),
                    this.notify(a)
                }
                ))
            }
        }),
        R(t.enableRequest, !0) && e.use({
            name: bt.BROWSER_XHR,
            run: function() {
                ir(this.options).subscribe((t => {
                    var e, n;
                    if (t.isInternal)
                        return;
                    const r = t.status >= 200 && t.status < 400;
                    if (_(t.url, this.options.ignoreRequestConfig, t.status))
                        return;
                    const o = w(t.url)
                      , i = {
                        start: 1e3 * t.start,
                        end: 1e3 * t.end,
                        duration: 1e3 * t.duration,
                        host: "",
                        kind: "client",
                        links: [],
                        logs: [],
                        name: `${t.method} ${null != o ? o.path : t.url}`,
                        parentSpanID: "",
                        spanID: t.spanID,
                        statusCode: r ? Rt.OK : Rt.ERROR,
                        statusMessage: null != (n = null == (e = t.xhr) ? void 0 : e.statusText) ? n : "",
                        traceID: t.traceID,
                        attribute: {
                            t: mt.API
                        },
                        resource: {}
                    }
                      , s = T(t.url, t.method, t.status, o);
                    dt(s, i.attribute, "http");
                    const a = {
                        otBase: i,
                        extra: {
                            start: t.start,
                            relativeTime: t.relativeTime,
                            duration: t.duration,
                            httpInfo: s,
                            httpContext: t
                        }
                    };
                    P(this.options.enableRequestBodyConfig, a, r) && (i.attribute["http.request.body"] = t.body),
                    this.notify(a)
                }
                ))
            }
        }),
        e.use(jn()),
        e.use((n = t.stsPlugin,
        {
            name: bt.BROWSER_SEND,
            run: function() {
                const t = new on({
                    project: this.options.project,
                    host: this.options.host,
                    logstore: this.options.logstore,
                    count: this.options.trackCountThreshold,
                    time: this.options.trackTimeThreshold
                });
                n && t.useStsPlugin(n),
                this.subscribe("*", ( (e, n) => {
                    const {otBase: r} = e;
                    t.send(r),
                    n(e)
                }
                ), gt[bt.BROWSER_SEND])
            }
        })),
        e.use({
            name: bt.BROWSER_LOCATION,
            run: function() {
                const t = (t, e) => {
                    const n = {
                        t: mt.LOCATION,
                        launch: t ? "true" : "false"
                    };
                    e && (Jn(e.newLocation, "to", n),
                    Jn(e.oldLocation, "from", n));
                    const r = {
                        start: 1e3 * L(),
                        attribute: n,
                        resource: {}
                    };
                    this.notify({
                        otBase: r,
                        extra: {}
                    })
                }
                ;
                t(!0),
                Kn(window.location).subscribe((e => {
                    this.session.refreshPageId(),
                    t(!1, e)
                }
                ))
            }
        }),
        R(t.enableRuntimeError, !0) && e.use(Xt()),
        R(t.enableResourceError, !0) && e.use({
            name: bt.BROWSER_RESOURCE_ERROR,
            run: function() {
                Jt(window, Kt.ERROE, (t => {
                    t.stopImmediatePropagation();
                    const e = t.target;
                    if (e != window && null != e) {
                        const r = e.src || e.href;
                        if (_(r, this.options.ignoreResourceConfig))
                            return;
                        const o = e.nodeName
                          , i = B(t.timeStamp)
                          , s = ke(r, "")
                          , a = {
                            t: mt.RESOURCE_ERROR
                        }
                          , c = {
                            start: 1e3 * i,
                            attribute: a,
                            resource: {}
                        };
                        dt({
                            type: s,
                            nodeName: (n = o,
                            "[object String]" === Object.prototype.toString.call(n) ? o.toLowerCase() : ""),
                            url: r,
                            id: y()
                        }, a, "resource"),
                        this.notify({
                            otBase: c,
                            extra: {}
                        })
                    }
                    var n
                }
                ), {
                    capture: !0
                })
            }
        }),
        R(t.enableDomClick, !0) && e.use(Mn()),
        e.use(Vt()),
        e.use({
            name: bt.BROWSER_CONSOLE,
            run: function() {
                Ue(this.options).subscribe((t => {
                    const e = {
                        t: mt.CONSOLE_LOG
                    };
                    dt(t, e, mt.CONSOLE_LOG);
                    const n = {
                        start: 1e3 * L(),
                        attribute: e,
                        resource: {}
                    };
                    this.notify({
                        otBase: n,
                        extra: {}
                    })
                }
                ))
            }
        }),
        e.use(Qe()),
        e
    }
    ), (t => ({
        addError: e => {
            const n = t.current;
            n && n.addError(e)
        }
    })));
    n(window, ht, ur, (t => {
        const e = window[ht];
        t(),
        e && (e.q && e.q.forEach((t => E(t, "onReady callback threw an error:")())),
        e.p && e.p.forEach((t => ur.addLog(t))),
        e.e && e.e.forEach((t => ur.addError(t))))
    }
    )),
    t.SLSBrowserClient = cr,
    t.SLS_CLIENT = ur
}(this["web-browser"] = this["web-browser"] || {});
//# sourceMappingURL=web-browser.global.js.map
