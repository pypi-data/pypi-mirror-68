(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[31],{2253:function(e,t,n){},2391:function(e,t,n){"use strict";n.r(t);var a=n(6),r=n(11),o=n(14),l=n(12),c=n(13),i=n(0),u=n.n(i),s=n(2378),p=n(2094),d=(n(2253),function(e){function t(){var e,n;Object(a.a)(this,t);for(var r=arguments.length,c=new Array(r),i=0;i<r;i++)c[i]=arguments[i];return(n=Object(o.a)(this,(e=Object(l.a)(t)).call.apply(e,[this].concat(c)))).state={value:n.props.element.get("default")},n.setWidgetValue=function(e){var t=n.props.element.get("id");n.props.widgetMgr.setStringValue(t,n.state.value,e)},n.onChangeComplete=function(e){n.setState({value:e.hex},function(){return n.setWidgetValue({fromUi:!0})})},n.render=function(){var e=n.props,t=e.element,a=e.width,r=n.state.value,o={width:a},l={backgroundColor:r,boxShadow:"".concat(r," 0px 0px 4px")},c=t.get("label");return u.a.createElement("div",{className:"Widget stColorPicker",style:o},u.a.createElement("label",null,c),u.a.createElement(s.a,{content:function(){return u.a.createElement(p.ChromePicker,{color:r,onChangeComplete:n.onChangeComplete,disableAlpha:!0})}},u.a.createElement("div",{className:"color-preview",style:l})))},n}return Object(c.a)(t,e),Object(r.a)(t,[{key:"componentDidMount",value:function(){this.setWidgetValue({fromUi:!1})}}]),t}(u.a.PureComponent));n.d(t,"default",function(){return d})}}]);
//# sourceMappingURL=31.70603cf3.chunk.js.map