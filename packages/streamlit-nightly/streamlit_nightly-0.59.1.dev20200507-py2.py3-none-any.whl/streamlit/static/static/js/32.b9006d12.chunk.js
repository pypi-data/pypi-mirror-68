(window["webpackJsonpstreamlit-browser"]=window["webpackJsonpstreamlit-browser"]||[]).push([[32],{2344:function(e,t,r){},2388:function(e,t,r){"use strict";r.r(t);var a=r(36),n=r(6),s=r(14),o=r(12),l=r(13),c=r(140),i=r.n(c),u=r(2369),d=r(62),p=r(155),m=r(0),g=r.n(m),f=r(4);r(2344);function v(e,t){var r=Object.keys(e);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(e);t&&(a=a.filter(function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable})),r.push.apply(r,a)}return r}function y(e){for(var t=1;t<arguments.length;t++){var r=null!=arguments[t]?arguments[t]:{};t%2?v(r,!0).forEach(function(t){Object(a.a)(e,t,r[t])}):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(r)):v(r).forEach(function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(r,t))})}return e}var b=function(e){function t(e){var r;return Object(n.a)(this,t),(r=Object(s.a)(this,Object(o.a)(t).call(this,e))).currentUploadCanceller=void 0,r.dropHandler=function(e,t,a){var n=r.props.element.get("maxUploadSizeMb");if(t.length>0){var s="".concat(t[0].type," files are not allowed");r.setState({status:"ERROR",errorMessage:s})}else{var o=1024*n*1024,l=!0,c=!1,u=void 0;try{for(var d,p=e[Symbol.iterator]();!(l=(d=p.next()).done);l=!0){if(d.value.size>o){var m="The max file size allowed is ".concat(n,"MB");return void r.setState({status:"ERROR",errorMessage:m})}}}catch(g){c=!0,u=g}finally{try{l||null==p.return||p.return()}finally{if(c)throw u}}r.setState({acceptedFiles:e,status:"UPLOADING"}),r.currentUploadCanceller=i.a.CancelToken.source(),r.props.uploadClient.uploadFiles(r.props.element.get("id"),e,void 0,r.currentUploadCanceller.token).then(function(){r.currentUploadCanceller=void 0,r.setState({status:"UPLOADED"})}).catch(function(e){i.a.isCancel(e)?(r.currentUploadCanceller=void 0,r.setState({status:"UPLOADED"})):r.setState({status:"ERROR",errorMessage:e?e.toString():"Unknown error"})})}},r.reset=function(){r.setState({status:"READY",errorMessage:void 0,acceptedFiles:[]})},r.renderErrorMessage=function(){var e=r.state.errorMessage;return g.a.createElement("div",{className:"uploadStatus uploadError"},g.a.createElement("span",{className:"body"},g.a.createElement(d.a,{className:"icon",type:"warning"})," ",e),g.a.createElement(f.Button,{color:"link",onClick:r.reset},"OK"))},r.renderUploadingMessage=function(){return g.a.createElement("div",{className:"uploadStatus uploadProgress"},g.a.createElement("span",{className:"body"},g.a.createElement(f.Spinner,{color:"secondary",size:"sm"})," Uploading..."),g.a.createElement(f.Button,{color:"link",onClick:r.cancelCurrentUpload},"Cancel"))},r.cancelCurrentUpload=function(){null!=r.currentUploadCanceller&&(r.currentUploadCanceller.cancel(),r.currentUploadCanceller=void 0)},r.renderFileUploader=function(){var e=r.state,t=e.status,a=e.errorMessage,n=r.props.element,s=n.get("type").toArray().map(function(e){return"."+e}),o=n.get("multipleFiles"),l=p.d,c="";return"UPLOADED"===t&&((l=y({},l)).ContentMessage=y({},l.ContentMessage),l.ContentMessage.style=y({},l.ContentMessage.style),l.ContentMessage.style.visibility="hidden",l.ContentMessage.style.overflow="hidden",l.ContentMessage.style.height="0.625rem",l.ContentSeparator=y({},l.ContentSeparator),l.ContentSeparator.style.visibility="hidden",c=o?r.state.acceptedFiles.map(function(e){return e.name}).join(", "):r.state.acceptedFiles[0].name),g.a.createElement(g.a.Fragment,null,"UPLOADED"===t&&g.a.createElement("div",{className:"uploadOverlay uploadDone"},g.a.createElement("span",{className:"body"},c)),g.a.createElement(u.a,{onDrop:r.dropHandler,errorMessage:a,accept:0===s.length?void 0:s,disabled:r.props.disabled,overrides:l,multiple:o}))},r.render=function(){var e=r.state.status,t=r.props.element.get("label");return g.a.createElement("div",{className:"Widget stFileUploader"},g.a.createElement("label",null,t),"ERROR"===e?r.renderErrorMessage():"UPLOADING"===e?r.renderUploadingMessage():r.renderFileUploader())},r.state={status:"READY",errorMessage:void 0,acceptedFiles:[]},r}return Object(l.a)(t,e),t}(g.a.PureComponent);r.d(t,"default",function(){return b})}}]);
//# sourceMappingURL=32.b9006d12.chunk.js.map