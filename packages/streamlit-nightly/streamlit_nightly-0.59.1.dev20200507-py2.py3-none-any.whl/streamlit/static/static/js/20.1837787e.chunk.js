(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[20],{2334:function(e,t,n){var r=n(2335),a=n(1549),o=n(1547),u=a(function(e,t){return o(e)?r(e,t):[]});e.exports=u},2335:function(e,t,n){var r=n(1526),a=n(2336),o=n(2341),u=n(1312),i=n(1209),l=n(1527),s=200;e.exports=function(e,t,n,c){var f=-1,p=a,v=!0,h=e.length,g=[],d=t.length;if(!h)return g;n&&(t=u(t,i(n))),c?(p=o,v=!1):t.length>=s&&(p=l,v=!1,t=new r(t));e:for(;++f<h;){var m=e[f],w=null==n?m:n(m);if(m=c||0!==m?m:0,v&&w===w){for(var b=d;b--;)if(t[b]===w)continue e;g.push(m)}else p(t,w,c)||g.push(m)}return g}},2336:function(e,t,n){var r=n(2337);e.exports=function(e,t){return!!(null==e?0:e.length)&&r(e,t,0)>-1}},2337:function(e,t,n){var r=n(2338),a=n(2339),o=n(2340);e.exports=function(e,t,n){return t===t?o(e,t,n):r(e,a,n)}},2338:function(e,t){e.exports=function(e,t,n,r){for(var a=e.length,o=n+(r?1:-1);r?o--:++o<a;)if(t(e[o],o,e))return o;return-1}},2339:function(e,t){e.exports=function(e){return e!==e}},2340:function(e,t){e.exports=function(e,t,n){for(var r=n-1,a=e.length;++r<a;)if(e[r]===t)return r;return-1}},2341:function(e,t){e.exports=function(e,t,n){for(var r=-1,a=null==e?0:e.length;++r<a;)if(n(t,e[r]))return!0;return!1}},2393:function(e,t,n){"use strict";n.r(t);var r=n(6),a=n(11),o=n(14),u=n(12),i=n(13),l=n(0),s=n.n(l),c=n(2334),f=n.n(c),p=n(155),v=n(2367),h=n(1229),g=function(e){function t(){var e,n;Object(r.a)(this,t);for(var a=arguments.length,i=new Array(a),l=0;l<a;l++)i[l]=arguments[l];return(n=Object(o.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(i)))).state={value:n.props.element.get("default").toArray()},n.setWidgetValue=function(e){var t=n.props.element.get("id");n.props.widgetMgr.setIntArrayValue(t,n.state.value,e)},n.onChange=function(e){var t=n.generateNewState(e);n.setState(t,function(){return n.setWidgetValue({fromUi:!0})})},n}return Object(i.a)(t,e),Object(a.a)(t,[{key:"componentDidMount",value:function(){this.setWidgetValue({fromUi:!1})}},{key:"generateNewState",value:function(e){var t=function(){var t=e.option.value;return parseInt(t,10)};switch(e.type){case"remove":return{value:f()(this.state.value,t())};case"clear":return{value:[]};case"select":return{value:this.state.value.concat([t()])};default:throw new Error("State transition is unkonwn: {data.type}")}}},{key:"render",value:function(){var e=this.props,t=e.element,n={width:e.width},r=t.get("label"),a=t.get("options"),o=0===a.size||this.props.disabled,u=0===a.size?"No options to select.":"Choose an option",i=a.map(function(e,t){return{label:e,value:t.toString()}}).toArray();return s.a.createElement("div",{className:"Widget row-widget stMultiSelect",style:n},s.a.createElement("label",null,r),s.a.createElement(v.a,{options:i,labelKey:"label",valueKey:"value",placeholder:u,type:h.b.select,multi:!0,onChange:this.onChange,value:this.valueFromState,disabled:o,size:"compact",overrides:p.f}))}},{key:"valueFromState",get:function(){var e=this;return this.state.value.map(function(t){var n=e.props.element.get("options").get(t);return{value:t.toString(),label:n}})}}]),t}(s.a.PureComponent);n.d(t,"default",function(){return g})}}]);
//# sourceMappingURL=20.1837787e.chunk.js.map