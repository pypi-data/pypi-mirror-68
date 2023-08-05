(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[19],{1231:function(t,e,n){"use strict";var r=n(6),a=n(14),i=n(12),o=n(13),c=n(0),s=n.n(c),u=n(135),p=n.n(u),l=n(19),h=n.n(l),b=n(25),f=n(11),w=n(32),m=function(){function t(){Object(r.a)(this,t)}return Object(f.a)(t,null,[{key:"get",value:function(){var e=Object(b.a)(h.a.mark(function e(){return h.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:if(null!=t.token){e.next=8;break}if(""===w.a.current.userMapboxToken){e.next=5;break}t.token=w.a.current.userMapboxToken,e.next=8;break;case 5:return e.next=7,this.fetchToken("https://data.streamlit.io/tokens.json","mapbox");case 7:t.token=e.sent;case 8:return e.abrupt("return",t.token);case 9:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}()},{key:"fetchToken",value:function(){var t=Object(b.a)(h.a.mark(function t(e,n){var r,a,i;return h.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,fetch(e);case 3:r=t.sent,t.next=9;break;case 6:throw t.prev=6,t.t0=t.catch(0),new Error("".concat(t.t0.message," (").concat(e,")"));case 9:if(r.ok){t.next=11;break}throw new Error("Bad status: ".concat(r.status," (").concat(e,")"));case 11:return t.next=13,r.json();case 13:if(a=t.sent,null!=(i=a[n])&&""!==i){t.next=17;break}throw new Error('Missing token "'.concat(n,'" (').concat(e,")"));case 17:return t.abrupt("return",i);case 18:case"end":return t.stop()}},t,null,[[0,6]])}));return function(e,n){return t.apply(this,arguments)}}()}]),t}();m.token=void 0;var k=n(208),d=n(209),g=n(45);e.a=function(t){var e=function(e){function n(e){var o;return Object(r.a)(this,n),(o=Object(a.a)(this,Object(i.a)(n).call(this,e))).initMapboxToken=function(){m.get().then(function(t){return o.setState({mapboxToken:t})}).catch(function(t){return o.setState({mapboxTokenError:t})})},o.render=function(){return null!=o.state.mapboxTokenError?s.a.createElement(k.a,{width:o.props.width,name:"Error fetching Mapbox token",message:o.state.mapboxTokenError.message}):void 0===o.state.mapboxToken?s.a.createElement(d.a,{element:Object(g.e)("Loading...").get("alert"),width:o.props.width}):s.a.createElement(t,Object.assign({mapboxToken:o.state.mapboxToken},o.props))},o.state={mapboxToken:void 0,mapboxTokenError:void 0},o.initMapboxToken(),o}return Object(o.a)(n,e),n}(c.PureComponent);return e.displayName="withMapboxToken(".concat(t.displayName||t.name,")"),p()(e,t)}},1362:function(t,e){},1367:function(t,e){},1369:function(t,e){},1377:function(t,e){},1397:function(t,e){},2001:function(t,e,n){},2374:function(t,e,n){"use strict";n.r(e);var r=n(6),a=n(11),i=n(14),o=n(12),c=n(13),s=n(36),u=n(0),p=n.n(u),l=n(1357),h=n.n(l),b=n(1347),f=n(1055),w=n(2014),m=n(1465),k=n(1470),d=n(2002),g=n(1096),O=n(214),v=n(1231);n(1356),n(2001);function j(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(t);e&&(r=r.filter(function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable})),n.push.apply(n,r)}return n}var x={classes:function(t){for(var e=1;e<arguments.length;e++){var n=null!=arguments[e]?arguments[e]:{};e%2?j(n,!0).forEach(function(e){Object(s.a)(t,e,n[e])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):j(n).forEach(function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(n,e))})}return t}({},f,{},m,{},k)};Object(g.registerLoaders)([d.CSVLoader]);var y=new w.JSONConverter({configuration:x}),S=500,T=function(t){function e(){var t,n;Object(r.a)(this,e);for(var a=arguments.length,c=new Array(a),s=0;s<a;s++)c[s]=arguments[s];return(n=Object(i.a)(this,(t=Object(o.a)(e)).call.apply(t,[this].concat(c)))).state={initialized:!1},n.componentDidMount=function(){n.setState({initialized:!0})},n.getDeckObject=function(){var t=n.props,e=t.element,r=t.width,a=t.height,i=e.get("useContainerWidth"),o=JSON.parse(e.get("json"));return a?(o.initialViewState.height=a,o.initialViewState.width=r):(o.initialViewState.height||(o.initialViewState.height=S),i&&(o.initialViewState.width=r)),delete o.views,y.convert(o)},n.createTooltip=function(t){var e=n.props.element.get("tooltip");return!!(t&&t.object&&e)&&((e=JSON.parse(e)).html?e.html=n.interpolate(t,e.html):e.text=n.interpolate(t,e.text),e)},n.interpolate=function(t,e){var n=e.match(/{(.*?)}/g);return n&&n.forEach(function(n){var r=n.substring(1,n.length-1);t.object.hasOwnProperty(r)&&(e=e.replace(n,t.object[r]))}),e},n}return Object(c.a)(e,t),Object(a.a)(e,[{key:"render",value:function(){var t=this.getDeckObject();return p.a.createElement("div",{className:"stDeckGlJsonChart",style:{height:t.initialViewState.height,width:t.initialViewState.width}},p.a.createElement(h.a,{initialViewState:t.initialViewState,height:t.initialViewState.height,width:t.initialViewState.width,layers:this.state.initialized?t.layers:[],getTooltip:this.createTooltip,controller:!0},p.a.createElement(b.StaticMap,{height:t.initialViewState.height,width:t.initialViewState.width,mapStyle:t.mapStyle?"string"===typeof t.mapStyle?t.mapStyle:t.mapStyle[0]:void 0,mapboxApiAccessToken:this.props.mapboxToken})))}}]),e}(u.PureComponent),E=Object(v.a)(Object(O.a)(T));n.d(e,"default",function(){return E})}}]);
//# sourceMappingURL=19.f6b4a668.chunk.js.map