(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[38],{2394:function(e,t,r){"use strict";r.r(t);var n=r(6),a=r(11),i=r(14),u=r(12),c=r(13),o=r(0),s=r.n(o),l=r(33),h=r(214),p=r(2050),f=r.n(p),g=450,d=function(e){function t(){var e,r;Object(n.a)(this,t);for(var a=arguments.length,c=new Array(a),o=0;o<a;o++)c[o]=arguments[o];return(r=Object(i.a)(this,(e=Object(u.a)(t)).call.apply(e,[this].concat(c)))).renderIFrame=function(e){var t=r.props.width,n=r.props.height?r.props.height:g;return s.a.createElement("iframe",{title:"Plotly",src:e,style:{width:t,height:n}})},r.isFullScreen=function(){return!!r.props.height},r.generateSpec=function(e){var t=r.props,n=t.element,a=t.height,i=t.width,u=JSON.parse(e.get("spec")),c=JSON.parse(n.get("useContainerWidth"));return r.isFullScreen()?(u.layout.width=i,u.layout.height=a):c&&(u.layout.width=i),u},r.renderFigure=function(e){var t=JSON.parse(e.get("config")),n=r.generateSpec(e),a=n.data,i=n.layout,u=n.frames;return s.a.createElement(f.a,{key:r.isFullScreen()?"fullscreen":"original",className:"stPlotlyChart",data:a,layout:i,config:t,frames:u})},r}return Object(c.a)(t,e),Object(a.a)(t,[{key:"render",value:function(){var e=this,t=this.props.element;return Object(l.a)(t,"chart",{url:function(t){return e.renderIFrame(t)},figure:function(t){return e.renderFigure(t)}})}}]),t}(o.PureComponent),w=Object(h.a)(d);r.d(t,"default",function(){return w})}}]);
//# sourceMappingURL=38.16e13e28.chunk.js.map