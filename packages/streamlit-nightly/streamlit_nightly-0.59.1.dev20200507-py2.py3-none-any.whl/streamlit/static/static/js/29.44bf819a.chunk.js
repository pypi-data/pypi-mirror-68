(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[29],{2342:function(t,e,i){},2392:function(t,e,i){"use strict";i.r(e);var n=i(6),s=i(11),r=i(14),a=i(12),o=i(13),u=i(0),l=i.n(u),c=i(4),w=(i(2342),50),h=function(t){function e(){var t,i;Object(n.a)(this,e);for(var s=arguments.length,o=new Array(s),u=0;u<s;u++)o[u]=arguments[u];return(i=Object(r.a)(this,(t=Object(a.a)(e)).call.apply(t,[this].concat(o)))).lastValue=-1,i.lastAnimatedTime=-1,i.isMovingBackwards=function(){return i.props.element.get("value")<i.lastValue},i.isMovingSuperFast=function(t,e){return t-e<w},i.isBrowserTabVisible=function(){return"hidden"===document.visibilityState},i.shouldUseTransition=function(t,e){return i.isMovingBackwards()||i.isMovingSuperFast(t,e)||i.isBrowserTabVisible()},i}return Object(o.a)(e,t),Object(s.a)(e,[{key:"render",value:function(){var t=this.props,e=t.element,i=t.width,n=e.get("value"),s=(new Date).getTime(),r=this.shouldUseTransition(s,this.lastAnimatedTime)?"without-transition":"with-transition";return"with-transition"===r&&(this.lastAnimatedTime=s),this.lastValue=n,l.a.createElement(c.Progress,{value:n,className:"stProgress "+r,style:{width:i}})}}]),e}(u.PureComponent);i.d(e,"default",function(){return h})}}]);
//# sourceMappingURL=29.44bf819a.chunk.js.map