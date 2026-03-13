(()=>{var G5=Object.create;var f_=Object.defineProperty;var V5=Object.getOwnPropertyDescriptor;var K5=Object.getOwnPropertyNames;var J5=Object.getPrototypeOf,W5=Object.prototype.hasOwnProperty;var Wt=(e,t)=>()=>(t||e((t={exports:{}}).exports,t),t.exports);var I5=(e,t,n,l)=>{if(t&&typeof t=="object"||typeof t=="function")for(let a of K5(t))!W5.call(e,a)&&a!==n&&f_(e,a,{get:()=>t[a],enumerable:!(l=V5(t,a))||l.enumerable});return e};var fn=(e,t,n)=>(n=e!=null?G5(J5(e)):{},I5(t||!e||!e.__esModule?f_(n,"default",{value:e,enumerable:!0}):n,e));var w_=Wt(Z=>{"use strict";var ku=Symbol.for("react.transitional.element"),F5=Symbol.for("react.portal"),P5=Symbol.for("react.fragment"),e2=Symbol.for("react.strict_mode"),t2=Symbol.for("react.profiler"),n2=Symbol.for("react.consumer"),l2=Symbol.for("react.context"),a2=Symbol.for("react.forward_ref"),o2=Symbol.for("react.suspense"),i2=Symbol.for("react.memo"),p_=Symbol.for("react.lazy"),s2=Symbol.for("react.activity"),m_=Symbol.iterator;function u2(e){return e===null||typeof e!="object"?null:(e=m_&&e[m_]||e["@@iterator"],typeof e=="function"?e:null)}var b_={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},v_=Object.assign,S_={};function Il(e,t,n){this.props=e,this.context=t,this.refs=S_,this.updater=n||b_}Il.prototype.isReactComponent={};Il.prototype.setState=function(e,t){if(typeof e!="object"&&typeof e!="function"&&e!=null)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,e,t,"setState")};Il.prototype.forceUpdate=function(e){this.updater.enqueueForceUpdate(this,e,"forceUpdate")};function x_(){}x_.prototype=Il.prototype;function Mu(e,t,n){this.props=e,this.context=t,this.refs=S_,this.updater=n||b_}var Au=Mu.prototype=new x_;Au.constructor=Mu;v_(Au,Il.prototype);Au.isPureReactComponent=!0;var h_=Array.isArray;function Tu(){}var Se={H:null,A:null,T:null,S:null},C_=Object.prototype.hasOwnProperty;function zu(e,t,n){var l=n.ref;return{$$typeof:ku,type:e,key:t,ref:l!==void 0?l:null,props:n}}function c2(e,t){return zu(e.type,t,e.props)}function Nu(e){return typeof e=="object"&&e!==null&&e.$$typeof===ku}function r2(e){var t={"=":"=0",":":"=2"};return"$"+e.replace(/[=:]/g,function(n){return t[n]})}var y_=/\/+/g;function Eu(e,t){return typeof e=="object"&&e!==null&&e.key!=null?r2(""+e.key):t.toString(36)}function d2(e){switch(e.status){case"fulfilled":return e.value;case"rejected":throw e.reason;default:switch(typeof e.status=="string"?e.then(Tu,Tu):(e.status="pending",e.then(function(t){e.status==="pending"&&(e.status="fulfilled",e.value=t)},function(t){e.status==="pending"&&(e.status="rejected",e.reason=t)})),e.status){case"fulfilled":return e.value;case"rejected":throw e.reason}}throw e}function Wl(e,t,n,l,a){var o=typeof e;(o==="undefined"||o==="boolean")&&(e=null);var i=!1;if(e===null)i=!0;else switch(o){case"bigint":case"string":case"number":i=!0;break;case"object":switch(e.$$typeof){case ku:case F5:i=!0;break;case p_:return i=e._init,Wl(i(e._payload),t,n,l,a)}}if(i)return a=a(e),i=l===""?"."+Eu(e,0):l,h_(a)?(n="",i!=null&&(n=i.replace(y_,"$&/")+"/"),Wl(a,t,n,"",function(h){return h})):a!=null&&(Nu(a)&&(a=c2(a,n+(a.key==null||e&&e.key===a.key?"":(""+a.key).replace(y_,"$&/")+"/")+i)),t.push(a)),1;i=0;var s=l===""?".":l+":";if(h_(e))for(var u=0;u<e.length;u++)l=e[u],o=s+Eu(l,u),i+=Wl(l,t,n,o,a);else if(u=u2(e),typeof u=="function")for(e=u.call(e),u=0;!(l=e.next()).done;)l=l.value,o=s+Eu(l,u++),i+=Wl(l,t,n,o,a);else if(o==="object"){if(typeof e.then=="function")return Wl(d2(e),t,n,l,a);throw t=String(e),Error("Objects are not valid as a React child (found: "+(t==="[object Object]"?"object with keys {"+Object.keys(e).join(", ")+"}":t)+"). If you meant to render a collection of children, use an array instead.")}return i}function vi(e,t,n){if(e==null)return e;var l=[],a=0;return Wl(e,l,"","",function(o){return t.call(n,o,a++)}),l}function _2(e){if(e._status===-1){var t=e._result;t=t(),t.then(function(n){(e._status===0||e._status===-1)&&(e._status=1,e._result=n)},function(n){(e._status===0||e._status===-1)&&(e._status=2,e._result=n)}),e._status===-1&&(e._status=0,e._result=t)}if(e._status===1)return e._result.default;throw e._result}var g_=typeof reportError=="function"?reportError:function(e){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var t=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof e=="object"&&e!==null&&typeof e.message=="string"?String(e.message):String(e),error:e});if(!window.dispatchEvent(t))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",e);return}console.error(e)},f2={map:vi,forEach:function(e,t,n){vi(e,function(){t.apply(this,arguments)},n)},count:function(e){var t=0;return vi(e,function(){t++}),t},toArray:function(e){return vi(e,function(t){return t})||[]},only:function(e){if(!Nu(e))throw Error("React.Children.only expected to receive a single React element child.");return e}};Z.Activity=s2;Z.Children=f2;Z.Component=Il;Z.Fragment=P5;Z.Profiler=t2;Z.PureComponent=Mu;Z.StrictMode=e2;Z.Suspense=o2;Z.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=Se;Z.__COMPILER_RUNTIME={__proto__:null,c:function(e){return Se.H.useMemoCache(e)}};Z.cache=function(e){return function(){return e.apply(null,arguments)}};Z.cacheSignal=function(){return null};Z.cloneElement=function(e,t,n){if(e==null)throw Error("The argument must be a React element, but you passed "+e+".");var l=v_({},e.props),a=e.key;if(t!=null)for(o in t.key!==void 0&&(a=""+t.key),t)!C_.call(t,o)||o==="key"||o==="__self"||o==="__source"||o==="ref"&&t.ref===void 0||(l[o]=t[o]);var o=arguments.length-2;if(o===1)l.children=n;else if(1<o){for(var i=Array(o),s=0;s<o;s++)i[s]=arguments[s+2];l.children=i}return zu(e.type,a,l)};Z.createContext=function(e){return e={$$typeof:l2,_currentValue:e,_currentValue2:e,_threadCount:0,Provider:null,Consumer:null},e.Provider=e,e.Consumer={$$typeof:n2,_context:e},e};Z.createElement=function(e,t,n){var l,a={},o=null;if(t!=null)for(l in t.key!==void 0&&(o=""+t.key),t)C_.call(t,l)&&l!=="key"&&l!=="__self"&&l!=="__source"&&(a[l]=t[l]);var i=arguments.length-2;if(i===1)a.children=n;else if(1<i){for(var s=Array(i),u=0;u<i;u++)s[u]=arguments[u+2];a.children=s}if(e&&e.defaultProps)for(l in i=e.defaultProps,i)a[l]===void 0&&(a[l]=i[l]);return zu(e,o,a)};Z.createRef=function(){return{current:null}};Z.forwardRef=function(e){return{$$typeof:a2,render:e}};Z.isValidElement=Nu;Z.lazy=function(e){return{$$typeof:p_,_payload:{_status:-1,_result:e},_init:_2}};Z.memo=function(e,t){return{$$typeof:i2,type:e,compare:t===void 0?null:t}};Z.startTransition=function(e){var t=Se.T,n={};Se.T=n;try{var l=e(),a=Se.S;a!==null&&a(n,l),typeof l=="object"&&l!==null&&typeof l.then=="function"&&l.then(Tu,g_)}catch(o){g_(o)}finally{t!==null&&n.types!==null&&(t.types=n.types),Se.T=t}};Z.unstable_useCacheRefresh=function(){return Se.H.useCacheRefresh()};Z.use=function(e){return Se.H.use(e)};Z.useActionState=function(e,t,n){return Se.H.useActionState(e,t,n)};Z.useCallback=function(e,t){return Se.H.useCallback(e,t)};Z.useContext=function(e){return Se.H.useContext(e)};Z.useDebugValue=function(){};Z.useDeferredValue=function(e,t){return Se.H.useDeferredValue(e,t)};Z.useEffect=function(e,t){return Se.H.useEffect(e,t)};Z.useEffectEvent=function(e){return Se.H.useEffectEvent(e)};Z.useId=function(){return Se.H.useId()};Z.useImperativeHandle=function(e,t,n){return Se.H.useImperativeHandle(e,t,n)};Z.useInsertionEffect=function(e,t){return Se.H.useInsertionEffect(e,t)};Z.useLayoutEffect=function(e,t){return Se.H.useLayoutEffect(e,t)};Z.useMemo=function(e,t){return Se.H.useMemo(e,t)};Z.useOptimistic=function(e,t){return Se.H.useOptimistic(e,t)};Z.useReducer=function(e,t,n){return Se.H.useReducer(e,t,n)};Z.useRef=function(e){return Se.H.useRef(e)};Z.useState=function(e){return Se.H.useState(e)};Z.useSyncExternalStore=function(e,t,n){return Se.H.useSyncExternalStore(e,t,n)};Z.useTransition=function(){return Se.H.useTransition()};Z.version="19.2.4"});var bl=Wt((ap,E_)=>{"use strict";E_.exports=w_()});var B_=Wt(Ee=>{"use strict";function Bu(e,t){var n=e.length;e.push(t);e:for(;0<n;){var l=n-1>>>1,a=e[l];if(0<Si(a,t))e[l]=t,e[n]=a,n=l;else break e}}function It(e){return e.length===0?null:e[0]}function Ci(e){if(e.length===0)return null;var t=e[0],n=e.pop();if(n!==t){e[0]=n;e:for(var l=0,a=e.length,o=a>>>1;l<o;){var i=2*(l+1)-1,s=e[i],u=i+1,h=e[u];if(0>Si(s,n))u<a&&0>Si(h,s)?(e[l]=h,e[u]=n,l=u):(e[l]=s,e[i]=n,l=i);else if(u<a&&0>Si(h,n))e[l]=h,e[u]=n,l=u;else break e}}return t}function Si(e,t){var n=e.sortIndex-t.sortIndex;return n!==0?n:e.id-t.id}Ee.unstable_now=void 0;typeof performance=="object"&&typeof performance.now=="function"?(T_=performance,Ee.unstable_now=function(){return T_.now()}):(Lu=Date,k_=Lu.now(),Ee.unstable_now=function(){return Lu.now()-k_});var T_,Lu,k_,mn=[],Rn=[],m2=1,zt=null,nt=3,Hu=!1,eo=!1,to=!1,Yu=!1,z_=typeof setTimeout=="function"?setTimeout:null,N_=typeof clearTimeout=="function"?clearTimeout:null,M_=typeof setImmediate<"u"?setImmediate:null;function xi(e){for(var t=It(Rn);t!==null;){if(t.callback===null)Ci(Rn);else if(t.startTime<=e)Ci(Rn),t.sortIndex=t.expirationTime,Bu(mn,t);else break;t=It(Rn)}}function Ru(e){if(to=!1,xi(e),!eo)if(It(mn)!==null)eo=!0,Pl||(Pl=!0,Fl());else{var t=It(Rn);t!==null&&Uu(Ru,t.startTime-e)}}var Pl=!1,no=-1,L_=5,O_=-1;function D_(){return Yu?!0:!(Ee.unstable_now()-O_<L_)}function Ou(){if(Yu=!1,Pl){var e=Ee.unstable_now();O_=e;var t=!0;try{e:{eo=!1,to&&(to=!1,N_(no),no=-1),Hu=!0;var n=nt;try{t:{for(xi(e),zt=It(mn);zt!==null&&!(zt.expirationTime>e&&D_());){var l=zt.callback;if(typeof l=="function"){zt.callback=null,nt=zt.priorityLevel;var a=l(zt.expirationTime<=e);if(e=Ee.unstable_now(),typeof a=="function"){zt.callback=a,xi(e),t=!0;break t}zt===It(mn)&&Ci(mn),xi(e)}else Ci(mn);zt=It(mn)}if(zt!==null)t=!0;else{var o=It(Rn);o!==null&&Uu(Ru,o.startTime-e),t=!1}}break e}finally{zt=null,nt=n,Hu=!1}t=void 0}}finally{t?Fl():Pl=!1}}}var Fl;typeof M_=="function"?Fl=function(){M_(Ou)}:typeof MessageChannel<"u"?(Du=new MessageChannel,A_=Du.port2,Du.port1.onmessage=Ou,Fl=function(){A_.postMessage(null)}):Fl=function(){z_(Ou,0)};var Du,A_;function Uu(e,t){no=z_(function(){e(Ee.unstable_now())},t)}Ee.unstable_IdlePriority=5;Ee.unstable_ImmediatePriority=1;Ee.unstable_LowPriority=4;Ee.unstable_NormalPriority=3;Ee.unstable_Profiling=null;Ee.unstable_UserBlockingPriority=2;Ee.unstable_cancelCallback=function(e){e.callback=null};Ee.unstable_forceFrameRate=function(e){0>e||125<e?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):L_=0<e?Math.floor(1e3/e):5};Ee.unstable_getCurrentPriorityLevel=function(){return nt};Ee.unstable_next=function(e){switch(nt){case 1:case 2:case 3:var t=3;break;default:t=nt}var n=nt;nt=t;try{return e()}finally{nt=n}};Ee.unstable_requestPaint=function(){Yu=!0};Ee.unstable_runWithPriority=function(e,t){switch(e){case 1:case 2:case 3:case 4:case 5:break;default:e=3}var n=nt;nt=e;try{return t()}finally{nt=n}};Ee.unstable_scheduleCallback=function(e,t,n){var l=Ee.unstable_now();switch(typeof n=="object"&&n!==null?(n=n.delay,n=typeof n=="number"&&0<n?l+n:l):n=l,e){case 1:var a=-1;break;case 2:a=250;break;case 5:a=1073741823;break;case 4:a=1e4;break;default:a=5e3}return a=n+a,e={id:m2++,callback:t,priorityLevel:e,startTime:n,expirationTime:a,sortIndex:-1},n>l?(e.sortIndex=n,Bu(Rn,e),It(mn)===null&&e===It(Rn)&&(to?(N_(no),no=-1):to=!0,Uu(Ru,n-l))):(e.sortIndex=a,Bu(mn,e),eo||Hu||(eo=!0,Pl||(Pl=!0,Fl()))),e};Ee.unstable_shouldYield=D_;Ee.unstable_wrapCallback=function(e){var t=nt;return function(){var n=nt;nt=t;try{return e.apply(this,arguments)}finally{nt=n}}}});var Y_=Wt((ip,H_)=>{"use strict";H_.exports=B_()});var U_=Wt(ot=>{"use strict";var h2=bl();function R_(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var n=2;n<arguments.length;n++)t+="&args[]="+encodeURIComponent(arguments[n])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function Un(){}var at={d:{f:Un,r:function(){throw Error(R_(522))},D:Un,C:Un,L:Un,m:Un,X:Un,S:Un,M:Un},p:0,findDOMNode:null},y2=Symbol.for("react.portal");function g2(e,t,n){var l=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:y2,key:l==null?null:""+l,children:e,containerInfo:t,implementation:n}}var lo=h2.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function wi(e,t){if(e==="font")return"";if(typeof t=="string")return t==="use-credentials"?t:""}ot.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=at;ot.createPortal=function(e,t){var n=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!t||t.nodeType!==1&&t.nodeType!==9&&t.nodeType!==11)throw Error(R_(299));return g2(e,t,null,n)};ot.flushSync=function(e){var t=lo.T,n=at.p;try{if(lo.T=null,at.p=2,e)return e()}finally{lo.T=t,at.p=n,at.d.f()}};ot.preconnect=function(e,t){typeof e=="string"&&(t?(t=t.crossOrigin,t=typeof t=="string"?t==="use-credentials"?t:"":void 0):t=null,at.d.C(e,t))};ot.prefetchDNS=function(e){typeof e=="string"&&at.d.D(e)};ot.preinit=function(e,t){if(typeof e=="string"&&t&&typeof t.as=="string"){var n=t.as,l=wi(n,t.crossOrigin),a=typeof t.integrity=="string"?t.integrity:void 0,o=typeof t.fetchPriority=="string"?t.fetchPriority:void 0;n==="style"?at.d.S(e,typeof t.precedence=="string"?t.precedence:void 0,{crossOrigin:l,integrity:a,fetchPriority:o}):n==="script"&&at.d.X(e,{crossOrigin:l,integrity:a,fetchPriority:o,nonce:typeof t.nonce=="string"?t.nonce:void 0})}};ot.preinitModule=function(e,t){if(typeof e=="string")if(typeof t=="object"&&t!==null){if(t.as==null||t.as==="script"){var n=wi(t.as,t.crossOrigin);at.d.M(e,{crossOrigin:n,integrity:typeof t.integrity=="string"?t.integrity:void 0,nonce:typeof t.nonce=="string"?t.nonce:void 0})}}else t==null&&at.d.M(e)};ot.preload=function(e,t){if(typeof e=="string"&&typeof t=="object"&&t!==null&&typeof t.as=="string"){var n=t.as,l=wi(n,t.crossOrigin);at.d.L(e,n,{crossOrigin:l,integrity:typeof t.integrity=="string"?t.integrity:void 0,nonce:typeof t.nonce=="string"?t.nonce:void 0,type:typeof t.type=="string"?t.type:void 0,fetchPriority:typeof t.fetchPriority=="string"?t.fetchPriority:void 0,referrerPolicy:typeof t.referrerPolicy=="string"?t.referrerPolicy:void 0,imageSrcSet:typeof t.imageSrcSet=="string"?t.imageSrcSet:void 0,imageSizes:typeof t.imageSizes=="string"?t.imageSizes:void 0,media:typeof t.media=="string"?t.media:void 0})}};ot.preloadModule=function(e,t){if(typeof e=="string")if(t){var n=wi(t.as,t.crossOrigin);at.d.m(e,{as:typeof t.as=="string"&&t.as!=="script"?t.as:void 0,crossOrigin:n,integrity:typeof t.integrity=="string"?t.integrity:void 0})}else at.d.m(e)};ot.requestFormReset=function(e){at.d.r(e)};ot.unstable_batchedUpdates=function(e,t){return e(t)};ot.useFormState=function(e,t,n){return lo.H.useFormState(e,t,n)};ot.useFormStatus=function(){return lo.H.useHostTransitionStatus()};ot.version="19.2.4"});var ju=Wt((up,X_)=>{"use strict";function j_(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(j_)}catch(e){console.error(e)}}j_(),X_.exports=U_()});var e5=Wt(Js=>{"use strict";var $e=Y_(),m1=bl(),p2=ju();function E(e){var t="https://react.dev/errors/"+e;if(1<arguments.length){t+="?args[]="+encodeURIComponent(arguments[1]);for(var n=2;n<arguments.length;n++)t+="&args[]="+encodeURIComponent(arguments[n])}return"Minified React error #"+e+"; visit "+t+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function h1(e){return!(!e||e.nodeType!==1&&e.nodeType!==9&&e.nodeType!==11)}function $o(e){var t=e,n=e;if(e.alternate)for(;t.return;)t=t.return;else{e=t;do t=e,(t.flags&4098)!==0&&(n=t.return),e=t.return;while(e)}return t.tag===3?n:null}function y1(e){if(e.tag===13){var t=e.memoizedState;if(t===null&&(e=e.alternate,e!==null&&(t=e.memoizedState)),t!==null)return t.dehydrated}return null}function g1(e){if(e.tag===31){var t=e.memoizedState;if(t===null&&(e=e.alternate,e!==null&&(t=e.memoizedState)),t!==null)return t.dehydrated}return null}function Q_(e){if($o(e)!==e)throw Error(E(188))}function b2(e){var t=e.alternate;if(!t){if(t=$o(e),t===null)throw Error(E(188));return t!==e?null:e}for(var n=e,l=t;;){var a=n.return;if(a===null)break;var o=a.alternate;if(o===null){if(l=a.return,l!==null){n=l;continue}break}if(a.child===o.child){for(o=a.child;o;){if(o===n)return Q_(a),e;if(o===l)return Q_(a),t;o=o.sibling}throw Error(E(188))}if(n.return!==l.return)n=a,l=o;else{for(var i=!1,s=a.child;s;){if(s===n){i=!0,n=a,l=o;break}if(s===l){i=!0,l=a,n=o;break}s=s.sibling}if(!i){for(s=o.child;s;){if(s===n){i=!0,n=o,l=a;break}if(s===l){i=!0,l=o,n=a;break}s=s.sibling}if(!i)throw Error(E(189))}}if(n.alternate!==l)throw Error(E(190))}if(n.tag!==3)throw Error(E(188));return n.stateNode.current===n?e:t}function p1(e){var t=e.tag;if(t===5||t===26||t===27||t===6)return e;for(e=e.child;e!==null;){if(t=p1(e),t!==null)return t;e=e.sibling}return null}var we=Object.assign,v2=Symbol.for("react.element"),Ei=Symbol.for("react.transitional.element"),_o=Symbol.for("react.portal"),oa=Symbol.for("react.fragment"),b1=Symbol.for("react.strict_mode"),vc=Symbol.for("react.profiler"),v1=Symbol.for("react.consumer"),xn=Symbol.for("react.context"),hr=Symbol.for("react.forward_ref"),Sc=Symbol.for("react.suspense"),xc=Symbol.for("react.suspense_list"),yr=Symbol.for("react.memo"),jn=Symbol.for("react.lazy"),Cc=Symbol.for("react.activity"),S2=Symbol.for("react.memo_cache_sentinel"),q_=Symbol.iterator;function ao(e){return e===null||typeof e!="object"?null:(e=q_&&e[q_]||e["@@iterator"],typeof e=="function"?e:null)}var x2=Symbol.for("react.client.reference");function wc(e){if(e==null)return null;if(typeof e=="function")return e.$$typeof===x2?null:e.displayName||e.name||null;if(typeof e=="string")return e;switch(e){case oa:return"Fragment";case vc:return"Profiler";case b1:return"StrictMode";case Sc:return"Suspense";case xc:return"SuspenseList";case Cc:return"Activity"}if(typeof e=="object")switch(e.$$typeof){case _o:return"Portal";case xn:return e.displayName||"Context";case v1:return(e._context.displayName||"Context")+".Consumer";case hr:var t=e.render;return e=e.displayName,e||(e=t.displayName||t.name||"",e=e!==""?"ForwardRef("+e+")":"ForwardRef"),e;case yr:return t=e.displayName||null,t!==null?t:wc(e.type)||"Memo";case jn:t=e._payload,e=e._init;try{return wc(e(t))}catch{}}return null}var fo=Array.isArray,j=m1.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,ce=p2.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,El={pending:!1,data:null,method:null,action:null},Ec=[],ia=-1;function nn(e){return{current:e}}function Ke(e){0>ia||(e.current=Ec[ia],Ec[ia]=null,ia--)}function ve(e,t){ia++,Ec[ia]=e.current,e.current=t}var tn=nn(null),zo=nn(null),In=nn(null),as=nn(null);function os(e,t){switch(ve(In,t),ve(zo,e),ve(tn,null),t.nodeType){case 9:case 11:e=(e=t.documentElement)&&(e=e.namespaceURI)?If(e):0;break;default:if(e=t.tagName,t=t.namespaceURI)t=If(t),e=jm(t,e);else switch(e){case"svg":e=1;break;case"math":e=2;break;default:e=0}}Ke(tn),ve(tn,e)}function wa(){Ke(tn),Ke(zo),Ke(In)}function Tc(e){e.memoizedState!==null&&ve(as,e);var t=tn.current,n=jm(t,e.type);t!==n&&(ve(zo,e),ve(tn,n))}function is(e){zo.current===e&&(Ke(tn),Ke(zo)),as.current===e&&(Ke(as),Xo._currentValue=El)}var Xu,$_;function Sl(e){if(Xu===void 0)try{throw Error()}catch(n){var t=n.stack.trim().match(/\n( *(at )?)/);Xu=t&&t[1]||"",$_=-1<n.stack.indexOf(`
    at`)?" (<anonymous>)":-1<n.stack.indexOf("@")?"@unknown:0:0":""}return`
`+Xu+e+$_}var Qu=!1;function qu(e,t){if(!e||Qu)return"";Qu=!0;var n=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{var l={DetermineComponentFrameRoot:function(){try{if(t){var S=function(){throw Error()};if(Object.defineProperty(S.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(S,[])}catch(b){var p=b}Reflect.construct(e,[],S)}else{try{S.call()}catch(b){p=b}e.call(S.prototype)}}else{try{throw Error()}catch(b){p=b}(S=e())&&typeof S.catch=="function"&&S.catch(function(){})}}catch(b){if(b&&p&&typeof b.stack=="string")return[b.stack,p.stack]}return[null,null]}};l.DetermineComponentFrameRoot.displayName="DetermineComponentFrameRoot";var a=Object.getOwnPropertyDescriptor(l.DetermineComponentFrameRoot,"name");a&&a.configurable&&Object.defineProperty(l.DetermineComponentFrameRoot,"name",{value:"DetermineComponentFrameRoot"});var o=l.DetermineComponentFrameRoot(),i=o[0],s=o[1];if(i&&s){var u=i.split(`
`),h=s.split(`
`);for(a=l=0;l<u.length&&!u[l].includes("DetermineComponentFrameRoot");)l++;for(;a<h.length&&!h[a].includes("DetermineComponentFrameRoot");)a++;if(l===u.length||a===h.length)for(l=u.length-1,a=h.length-1;1<=l&&0<=a&&u[l]!==h[a];)a--;for(;1<=l&&0<=a;l--,a--)if(u[l]!==h[a]){if(l!==1||a!==1)do if(l--,a--,0>a||u[l]!==h[a]){var y=`
`+u[l].replace(" at new "," at ");return e.displayName&&y.includes("<anonymous>")&&(y=y.replace("<anonymous>",e.displayName)),y}while(1<=l&&0<=a);break}}}finally{Qu=!1,Error.prepareStackTrace=n}return(n=e?e.displayName||e.name:"")?Sl(n):""}function C2(e,t){switch(e.tag){case 26:case 27:case 5:return Sl(e.type);case 16:return Sl("Lazy");case 13:return e.child!==t&&t!==null?Sl("Suspense Fallback"):Sl("Suspense");case 19:return Sl("SuspenseList");case 0:case 15:return qu(e.type,!1);case 11:return qu(e.type.render,!1);case 1:return qu(e.type,!0);case 31:return Sl("Activity");default:return""}}function Z_(e){try{var t="",n=null;do t+=C2(e,n),n=e,e=e.return;while(e);return t}catch(l){return`
Error generating stack: `+l.message+`
`+l.stack}}var kc=Object.prototype.hasOwnProperty,gr=$e.unstable_scheduleCallback,$u=$e.unstable_cancelCallback,w2=$e.unstable_shouldYield,E2=$e.unstable_requestPaint,wt=$e.unstable_now,T2=$e.unstable_getCurrentPriorityLevel,S1=$e.unstable_ImmediatePriority,x1=$e.unstable_UserBlockingPriority,ss=$e.unstable_NormalPriority,k2=$e.unstable_LowPriority,C1=$e.unstable_IdlePriority,M2=$e.log,A2=$e.unstable_setDisableYieldValue,Zo=null,Et=null;function Gn(e){if(typeof M2=="function"&&A2(e),Et&&typeof Et.setStrictMode=="function")try{Et.setStrictMode(Zo,e)}catch{}}var Tt=Math.clz32?Math.clz32:L2,z2=Math.log,N2=Math.LN2;function L2(e){return e>>>=0,e===0?32:31-(z2(e)/N2|0)|0}var Ti=256,ki=262144,Mi=4194304;function xl(e){var t=e&42;if(t!==0)return t;switch(e&-e){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:return 64;case 128:return 128;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:return e&261888;case 262144:case 524288:case 1048576:case 2097152:return e&3932160;case 4194304:case 8388608:case 16777216:case 33554432:return e&62914560;case 67108864:return 67108864;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 0;default:return e}}function Os(e,t,n){var l=e.pendingLanes;if(l===0)return 0;var a=0,o=e.suspendedLanes,i=e.pingedLanes;e=e.warmLanes;var s=l&134217727;return s!==0?(l=s&~o,l!==0?a=xl(l):(i&=s,i!==0?a=xl(i):n||(n=s&~e,n!==0&&(a=xl(n))))):(s=l&~o,s!==0?a=xl(s):i!==0?a=xl(i):n||(n=l&~e,n!==0&&(a=xl(n)))),a===0?0:t!==0&&t!==a&&(t&o)===0&&(o=a&-a,n=t&-t,o>=n||o===32&&(n&4194048)!==0)?t:a}function Go(e,t){return(e.pendingLanes&~(e.suspendedLanes&~e.pingedLanes)&t)===0}function O2(e,t){switch(e){case 1:case 2:case 4:case 8:case 64:return t+250;case 16:case 32:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return t+5e3;case 4194304:case 8388608:case 16777216:case 33554432:return-1;case 67108864:case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function w1(){var e=Mi;return Mi<<=1,(Mi&62914560)===0&&(Mi=4194304),e}function Zu(e){for(var t=[],n=0;31>n;n++)t.push(e);return t}function Vo(e,t){e.pendingLanes|=t,t!==268435456&&(e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0)}function D2(e,t,n,l,a,o){var i=e.pendingLanes;e.pendingLanes=n,e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0,e.expiredLanes&=n,e.entangledLanes&=n,e.errorRecoveryDisabledLanes&=n,e.shellSuspendCounter=0;var s=e.entanglements,u=e.expirationTimes,h=e.hiddenUpdates;for(n=i&~n;0<n;){var y=31-Tt(n),S=1<<y;s[y]=0,u[y]=-1;var p=h[y];if(p!==null)for(h[y]=null,y=0;y<p.length;y++){var b=p[y];b!==null&&(b.lane&=-536870913)}n&=~S}l!==0&&E1(e,l,0),o!==0&&a===0&&e.tag!==0&&(e.suspendedLanes|=o&~(i&~t))}function E1(e,t,n){e.pendingLanes|=t,e.suspendedLanes&=~t;var l=31-Tt(t);e.entangledLanes|=t,e.entanglements[l]=e.entanglements[l]|1073741824|n&261930}function T1(e,t){var n=e.entangledLanes|=t;for(e=e.entanglements;n;){var l=31-Tt(n),a=1<<l;a&t|e[l]&t&&(e[l]|=t),n&=~a}}function k1(e,t){var n=t&-t;return n=(n&42)!==0?1:pr(n),(n&(e.suspendedLanes|t))!==0?0:n}function pr(e){switch(e){case 2:e=1;break;case 8:e=4;break;case 32:e=16;break;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:e=128;break;case 268435456:e=134217728;break;default:e=0}return e}function br(e){return e&=-e,2<e?8<e?(e&134217727)!==0?32:268435456:8:2}function M1(){var e=ce.p;return e!==0?e:(e=window.event,e===void 0?32:Im(e.type))}function G_(e,t){var n=ce.p;try{return ce.p=e,t()}finally{ce.p=n}}var rl=Math.random().toString(36).slice(2),We="__reactFiber$"+rl,mt="__reactProps$"+rl,Ba="__reactContainer$"+rl,Mc="__reactEvents$"+rl,B2="__reactListeners$"+rl,H2="__reactHandles$"+rl,V_="__reactResources$"+rl,Ko="__reactMarker$"+rl;function vr(e){delete e[We],delete e[mt],delete e[Mc],delete e[B2],delete e[H2]}function sa(e){var t=e[We];if(t)return t;for(var n=e.parentNode;n;){if(t=n[Ba]||n[We]){if(n=t.alternate,t.child!==null||n!==null&&n.child!==null)for(e=n1(e);e!==null;){if(n=e[We])return n;e=n1(e)}return t}e=n,n=e.parentNode}return null}function Ha(e){if(e=e[We]||e[Ba]){var t=e.tag;if(t===5||t===6||t===13||t===31||t===26||t===27||t===3)return e}return null}function mo(e){var t=e.tag;if(t===5||t===26||t===27||t===6)return e.stateNode;throw Error(E(33))}function ga(e){var t=e[V_];return t||(t=e[V_]={hoistableStyles:new Map,hoistableScripts:new Map}),t}function Ve(e){e[Ko]=!0}var A1=new Set,z1={};function Bl(e,t){Ea(e,t),Ea(e+"Capture",t)}function Ea(e,t){for(z1[e]=t,e=0;e<t.length;e++)A1.add(t[e])}var Y2=RegExp("^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"),K_={},J_={};function R2(e){return kc.call(J_,e)?!0:kc.call(K_,e)?!1:Y2.test(e)?J_[e]=!0:(K_[e]=!0,!1)}function qi(e,t,n){if(R2(t))if(n===null)e.removeAttribute(t);else{switch(typeof n){case"undefined":case"function":case"symbol":e.removeAttribute(t);return;case"boolean":var l=t.toLowerCase().slice(0,5);if(l!=="data-"&&l!=="aria-"){e.removeAttribute(t);return}}e.setAttribute(t,""+n)}}function Ai(e,t,n){if(n===null)e.removeAttribute(t);else{switch(typeof n){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(t);return}e.setAttribute(t,""+n)}}function hn(e,t,n,l){if(l===null)e.removeAttribute(n);else{switch(typeof l){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(n);return}e.setAttributeNS(t,n,""+l)}}function Lt(e){switch(typeof e){case"bigint":case"boolean":case"number":case"string":case"undefined":return e;case"object":return e;default:return""}}function N1(e){var t=e.type;return(e=e.nodeName)&&e.toLowerCase()==="input"&&(t==="checkbox"||t==="radio")}function U2(e,t,n){var l=Object.getOwnPropertyDescriptor(e.constructor.prototype,t);if(!e.hasOwnProperty(t)&&typeof l<"u"&&typeof l.get=="function"&&typeof l.set=="function"){var a=l.get,o=l.set;return Object.defineProperty(e,t,{configurable:!0,get:function(){return a.call(this)},set:function(i){n=""+i,o.call(this,i)}}),Object.defineProperty(e,t,{enumerable:l.enumerable}),{getValue:function(){return n},setValue:function(i){n=""+i},stopTracking:function(){e._valueTracker=null,delete e[t]}}}}function Ac(e){if(!e._valueTracker){var t=N1(e)?"checked":"value";e._valueTracker=U2(e,t,""+e[t])}}function L1(e){if(!e)return!1;var t=e._valueTracker;if(!t)return!0;var n=t.getValue(),l="";return e&&(l=N1(e)?e.checked?"true":"false":e.value),e=l,e!==n?(t.setValue(e),!0):!1}function us(e){if(e=e||(typeof document<"u"?document:void 0),typeof e>"u")return null;try{return e.activeElement||e.body}catch{return e.body}}var j2=/[\n"\\]/g;function Bt(e){return e.replace(j2,function(t){return"\\"+t.charCodeAt(0).toString(16)+" "})}function zc(e,t,n,l,a,o,i,s){e.name="",i!=null&&typeof i!="function"&&typeof i!="symbol"&&typeof i!="boolean"?e.type=i:e.removeAttribute("type"),t!=null?i==="number"?(t===0&&e.value===""||e.value!=t)&&(e.value=""+Lt(t)):e.value!==""+Lt(t)&&(e.value=""+Lt(t)):i!=="submit"&&i!=="reset"||e.removeAttribute("value"),t!=null?Nc(e,i,Lt(t)):n!=null?Nc(e,i,Lt(n)):l!=null&&e.removeAttribute("value"),a==null&&o!=null&&(e.defaultChecked=!!o),a!=null&&(e.checked=a&&typeof a!="function"&&typeof a!="symbol"),s!=null&&typeof s!="function"&&typeof s!="symbol"&&typeof s!="boolean"?e.name=""+Lt(s):e.removeAttribute("name")}function O1(e,t,n,l,a,o,i,s){if(o!=null&&typeof o!="function"&&typeof o!="symbol"&&typeof o!="boolean"&&(e.type=o),t!=null||n!=null){if(!(o!=="submit"&&o!=="reset"||t!=null)){Ac(e);return}n=n!=null?""+Lt(n):"",t=t!=null?""+Lt(t):n,s||t===e.value||(e.value=t),e.defaultValue=t}l=l??a,l=typeof l!="function"&&typeof l!="symbol"&&!!l,e.checked=s?e.checked:!!l,e.defaultChecked=!!l,i!=null&&typeof i!="function"&&typeof i!="symbol"&&typeof i!="boolean"&&(e.name=i),Ac(e)}function Nc(e,t,n){t==="number"&&us(e.ownerDocument)===e||e.defaultValue===""+n||(e.defaultValue=""+n)}function pa(e,t,n,l){if(e=e.options,t){t={};for(var a=0;a<n.length;a++)t["$"+n[a]]=!0;for(n=0;n<e.length;n++)a=t.hasOwnProperty("$"+e[n].value),e[n].selected!==a&&(e[n].selected=a),a&&l&&(e[n].defaultSelected=!0)}else{for(n=""+Lt(n),t=null,a=0;a<e.length;a++){if(e[a].value===n){e[a].selected=!0,l&&(e[a].defaultSelected=!0);return}t!==null||e[a].disabled||(t=e[a])}t!==null&&(t.selected=!0)}}function D1(e,t,n){if(t!=null&&(t=""+Lt(t),t!==e.value&&(e.value=t),n==null)){e.defaultValue!==t&&(e.defaultValue=t);return}e.defaultValue=n!=null?""+Lt(n):""}function B1(e,t,n,l){if(t==null){if(l!=null){if(n!=null)throw Error(E(92));if(fo(l)){if(1<l.length)throw Error(E(93));l=l[0]}n=l}n==null&&(n=""),t=n}n=Lt(t),e.defaultValue=n,l=e.textContent,l===n&&l!==""&&l!==null&&(e.value=l),Ac(e)}function Ta(e,t){if(t){var n=e.firstChild;if(n&&n===e.lastChild&&n.nodeType===3){n.nodeValue=t;return}}e.textContent=t}var X2=new Set("animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(" "));function W_(e,t,n){var l=t.indexOf("--")===0;n==null||typeof n=="boolean"||n===""?l?e.setProperty(t,""):t==="float"?e.cssFloat="":e[t]="":l?e.setProperty(t,n):typeof n!="number"||n===0||X2.has(t)?t==="float"?e.cssFloat=n:e[t]=(""+n).trim():e[t]=n+"px"}function H1(e,t,n){if(t!=null&&typeof t!="object")throw Error(E(62));if(e=e.style,n!=null){for(var l in n)!n.hasOwnProperty(l)||t!=null&&t.hasOwnProperty(l)||(l.indexOf("--")===0?e.setProperty(l,""):l==="float"?e.cssFloat="":e[l]="");for(var a in t)l=t[a],t.hasOwnProperty(a)&&n[a]!==l&&W_(e,a,l)}else for(var o in t)t.hasOwnProperty(o)&&W_(e,o,t[o])}function Sr(e){if(e.indexOf("-")===-1)return!1;switch(e){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var Q2=new Map([["acceptCharset","accept-charset"],["htmlFor","for"],["httpEquiv","http-equiv"],["crossOrigin","crossorigin"],["accentHeight","accent-height"],["alignmentBaseline","alignment-baseline"],["arabicForm","arabic-form"],["baselineShift","baseline-shift"],["capHeight","cap-height"],["clipPath","clip-path"],["clipRule","clip-rule"],["colorInterpolation","color-interpolation"],["colorInterpolationFilters","color-interpolation-filters"],["colorProfile","color-profile"],["colorRendering","color-rendering"],["dominantBaseline","dominant-baseline"],["enableBackground","enable-background"],["fillOpacity","fill-opacity"],["fillRule","fill-rule"],["floodColor","flood-color"],["floodOpacity","flood-opacity"],["fontFamily","font-family"],["fontSize","font-size"],["fontSizeAdjust","font-size-adjust"],["fontStretch","font-stretch"],["fontStyle","font-style"],["fontVariant","font-variant"],["fontWeight","font-weight"],["glyphName","glyph-name"],["glyphOrientationHorizontal","glyph-orientation-horizontal"],["glyphOrientationVertical","glyph-orientation-vertical"],["horizAdvX","horiz-adv-x"],["horizOriginX","horiz-origin-x"],["imageRendering","image-rendering"],["letterSpacing","letter-spacing"],["lightingColor","lighting-color"],["markerEnd","marker-end"],["markerMid","marker-mid"],["markerStart","marker-start"],["overlinePosition","overline-position"],["overlineThickness","overline-thickness"],["paintOrder","paint-order"],["panose-1","panose-1"],["pointerEvents","pointer-events"],["renderingIntent","rendering-intent"],["shapeRendering","shape-rendering"],["stopColor","stop-color"],["stopOpacity","stop-opacity"],["strikethroughPosition","strikethrough-position"],["strikethroughThickness","strikethrough-thickness"],["strokeDasharray","stroke-dasharray"],["strokeDashoffset","stroke-dashoffset"],["strokeLinecap","stroke-linecap"],["strokeLinejoin","stroke-linejoin"],["strokeMiterlimit","stroke-miterlimit"],["strokeOpacity","stroke-opacity"],["strokeWidth","stroke-width"],["textAnchor","text-anchor"],["textDecoration","text-decoration"],["textRendering","text-rendering"],["transformOrigin","transform-origin"],["underlinePosition","underline-position"],["underlineThickness","underline-thickness"],["unicodeBidi","unicode-bidi"],["unicodeRange","unicode-range"],["unitsPerEm","units-per-em"],["vAlphabetic","v-alphabetic"],["vHanging","v-hanging"],["vIdeographic","v-ideographic"],["vMathematical","v-mathematical"],["vectorEffect","vector-effect"],["vertAdvY","vert-adv-y"],["vertOriginX","vert-origin-x"],["vertOriginY","vert-origin-y"],["wordSpacing","word-spacing"],["writingMode","writing-mode"],["xmlnsXlink","xmlns:xlink"],["xHeight","x-height"]]),q2=/^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;function $i(e){return q2.test(""+e)?"javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')":e}function Cn(){}var Lc=null;function xr(e){return e=e.target||e.srcElement||window,e.correspondingUseElement&&(e=e.correspondingUseElement),e.nodeType===3?e.parentNode:e}var ua=null,ba=null;function I_(e){var t=Ha(e);if(t&&(e=t.stateNode)){var n=e[mt]||null;e:switch(e=t.stateNode,t.type){case"input":if(zc(e,n.value,n.defaultValue,n.defaultValue,n.checked,n.defaultChecked,n.type,n.name),t=n.name,n.type==="radio"&&t!=null){for(n=e;n.parentNode;)n=n.parentNode;for(n=n.querySelectorAll('input[name="'+Bt(""+t)+'"][type="radio"]'),t=0;t<n.length;t++){var l=n[t];if(l!==e&&l.form===e.form){var a=l[mt]||null;if(!a)throw Error(E(90));zc(l,a.value,a.defaultValue,a.defaultValue,a.checked,a.defaultChecked,a.type,a.name)}}for(t=0;t<n.length;t++)l=n[t],l.form===e.form&&L1(l)}break e;case"textarea":D1(e,n.value,n.defaultValue);break e;case"select":t=n.value,t!=null&&pa(e,!!n.multiple,t,!1)}}}var Gu=!1;function Y1(e,t,n){if(Gu)return e(t,n);Gu=!0;try{var l=e(t);return l}finally{if(Gu=!1,(ua!==null||ba!==null)&&(Zs(),ua&&(t=ua,e=ba,ba=ua=null,I_(t),e)))for(t=0;t<e.length;t++)I_(e[t])}}function No(e,t){var n=e.stateNode;if(n===null)return null;var l=n[mt]||null;if(l===null)return null;n=l[t];e:switch(t){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(l=!l.disabled)||(e=e.type,l=!(e==="button"||e==="input"||e==="select"||e==="textarea")),e=!l;break e;default:e=!1}if(e)return null;if(n&&typeof n!="function")throw Error(E(231,t,typeof n));return n}var Mn=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),Oc=!1;if(Mn)try{ea={},Object.defineProperty(ea,"passive",{get:function(){Oc=!0}}),window.addEventListener("test",ea,ea),window.removeEventListener("test",ea,ea)}catch{Oc=!1}var ea,Vn=null,Cr=null,Zi=null;function R1(){if(Zi)return Zi;var e,t=Cr,n=t.length,l,a="value"in Vn?Vn.value:Vn.textContent,o=a.length;for(e=0;e<n&&t[e]===a[e];e++);var i=n-e;for(l=1;l<=i&&t[n-l]===a[o-l];l++);return Zi=a.slice(e,1<l?1-l:void 0)}function Gi(e){var t=e.keyCode;return"charCode"in e?(e=e.charCode,e===0&&t===13&&(e=13)):e=t,e===10&&(e=13),32<=e||e===13?e:0}function zi(){return!0}function F_(){return!1}function ht(e){function t(n,l,a,o,i){this._reactName=n,this._targetInst=a,this.type=l,this.nativeEvent=o,this.target=i,this.currentTarget=null;for(var s in e)e.hasOwnProperty(s)&&(n=e[s],this[s]=n?n(o):o[s]);return this.isDefaultPrevented=(o.defaultPrevented!=null?o.defaultPrevented:o.returnValue===!1)?zi:F_,this.isPropagationStopped=F_,this}return we(t.prototype,{preventDefault:function(){this.defaultPrevented=!0;var n=this.nativeEvent;n&&(n.preventDefault?n.preventDefault():typeof n.returnValue!="unknown"&&(n.returnValue=!1),this.isDefaultPrevented=zi)},stopPropagation:function(){var n=this.nativeEvent;n&&(n.stopPropagation?n.stopPropagation():typeof n.cancelBubble!="unknown"&&(n.cancelBubble=!0),this.isPropagationStopped=zi)},persist:function(){},isPersistent:zi}),t}var Hl={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(e){return e.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},Ds=ht(Hl),Jo=we({},Hl,{view:0,detail:0}),$2=ht(Jo),Vu,Ku,oo,Bs=we({},Jo,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:wr,button:0,buttons:0,relatedTarget:function(e){return e.relatedTarget===void 0?e.fromElement===e.srcElement?e.toElement:e.fromElement:e.relatedTarget},movementX:function(e){return"movementX"in e?e.movementX:(e!==oo&&(oo&&e.type==="mousemove"?(Vu=e.screenX-oo.screenX,Ku=e.screenY-oo.screenY):Ku=Vu=0,oo=e),Vu)},movementY:function(e){return"movementY"in e?e.movementY:Ku}}),P_=ht(Bs),Z2=we({},Bs,{dataTransfer:0}),G2=ht(Z2),V2=we({},Jo,{relatedTarget:0}),Ju=ht(V2),K2=we({},Hl,{animationName:0,elapsedTime:0,pseudoElement:0}),J2=ht(K2),W2=we({},Hl,{clipboardData:function(e){return"clipboardData"in e?e.clipboardData:window.clipboardData}}),I2=ht(W2),F2=we({},Hl,{data:0}),ef=ht(F2),P2={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},eh={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},th={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function nh(e){var t=this.nativeEvent;return t.getModifierState?t.getModifierState(e):(e=th[e])?!!t[e]:!1}function wr(){return nh}var lh=we({},Jo,{key:function(e){if(e.key){var t=P2[e.key]||e.key;if(t!=="Unidentified")return t}return e.type==="keypress"?(e=Gi(e),e===13?"Enter":String.fromCharCode(e)):e.type==="keydown"||e.type==="keyup"?eh[e.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:wr,charCode:function(e){return e.type==="keypress"?Gi(e):0},keyCode:function(e){return e.type==="keydown"||e.type==="keyup"?e.keyCode:0},which:function(e){return e.type==="keypress"?Gi(e):e.type==="keydown"||e.type==="keyup"?e.keyCode:0}}),ah=ht(lh),oh=we({},Bs,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),tf=ht(oh),ih=we({},Jo,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:wr}),sh=ht(ih),uh=we({},Hl,{propertyName:0,elapsedTime:0,pseudoElement:0}),ch=ht(uh),rh=we({},Bs,{deltaX:function(e){return"deltaX"in e?e.deltaX:"wheelDeltaX"in e?-e.wheelDeltaX:0},deltaY:function(e){return"deltaY"in e?e.deltaY:"wheelDeltaY"in e?-e.wheelDeltaY:"wheelDelta"in e?-e.wheelDelta:0},deltaZ:0,deltaMode:0}),dh=ht(rh),_h=we({},Hl,{newState:0,oldState:0}),fh=ht(_h),mh=[9,13,27,32],Er=Mn&&"CompositionEvent"in window,go=null;Mn&&"documentMode"in document&&(go=document.documentMode);var hh=Mn&&"TextEvent"in window&&!go,U1=Mn&&(!Er||go&&8<go&&11>=go),nf=" ",lf=!1;function j1(e,t){switch(e){case"keyup":return mh.indexOf(t.keyCode)!==-1;case"keydown":return t.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function X1(e){return e=e.detail,typeof e=="object"&&"data"in e?e.data:null}var ca=!1;function yh(e,t){switch(e){case"compositionend":return X1(t);case"keypress":return t.which!==32?null:(lf=!0,nf);case"textInput":return e=t.data,e===nf&&lf?null:e;default:return null}}function gh(e,t){if(ca)return e==="compositionend"||!Er&&j1(e,t)?(e=R1(),Zi=Cr=Vn=null,ca=!1,e):null;switch(e){case"paste":return null;case"keypress":if(!(t.ctrlKey||t.altKey||t.metaKey)||t.ctrlKey&&t.altKey){if(t.char&&1<t.char.length)return t.char;if(t.which)return String.fromCharCode(t.which)}return null;case"compositionend":return U1&&t.locale!=="ko"?null:t.data;default:return null}}var ph={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function af(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t==="input"?!!ph[e.type]:t==="textarea"}function Q1(e,t,n,l){ua?ba?ba.push(l):ba=[l]:ua=l,t=Ts(t,"onChange"),0<t.length&&(n=new Ds("onChange","change",null,n,l),e.push({event:n,listeners:t}))}var po=null,Lo=null;function bh(e){Ym(e,0)}function Hs(e){var t=mo(e);if(L1(t))return e}function of(e,t){if(e==="change")return t}var q1=!1;Mn&&(Mn?(Li="oninput"in document,Li||(Wu=document.createElement("div"),Wu.setAttribute("oninput","return;"),Li=typeof Wu.oninput=="function"),Ni=Li):Ni=!1,q1=Ni&&(!document.documentMode||9<document.documentMode));var Ni,Li,Wu;function sf(){po&&(po.detachEvent("onpropertychange",$1),Lo=po=null)}function $1(e){if(e.propertyName==="value"&&Hs(Lo)){var t=[];Q1(t,Lo,e,xr(e)),Y1(bh,t)}}function vh(e,t,n){e==="focusin"?(sf(),po=t,Lo=n,po.attachEvent("onpropertychange",$1)):e==="focusout"&&sf()}function Sh(e){if(e==="selectionchange"||e==="keyup"||e==="keydown")return Hs(Lo)}function xh(e,t){if(e==="click")return Hs(t)}function Ch(e,t){if(e==="input"||e==="change")return Hs(t)}function wh(e,t){return e===t&&(e!==0||1/e===1/t)||e!==e&&t!==t}var Mt=typeof Object.is=="function"?Object.is:wh;function Oo(e,t){if(Mt(e,t))return!0;if(typeof e!="object"||e===null||typeof t!="object"||t===null)return!1;var n=Object.keys(e),l=Object.keys(t);if(n.length!==l.length)return!1;for(l=0;l<n.length;l++){var a=n[l];if(!kc.call(t,a)||!Mt(e[a],t[a]))return!1}return!0}function uf(e){for(;e&&e.firstChild;)e=e.firstChild;return e}function cf(e,t){var n=uf(e);e=0;for(var l;n;){if(n.nodeType===3){if(l=e+n.textContent.length,e<=t&&l>=t)return{node:n,offset:t-e};e=l}e:{for(;n;){if(n.nextSibling){n=n.nextSibling;break e}n=n.parentNode}n=void 0}n=uf(n)}}function Z1(e,t){return e&&t?e===t?!0:e&&e.nodeType===3?!1:t&&t.nodeType===3?Z1(e,t.parentNode):"contains"in e?e.contains(t):e.compareDocumentPosition?!!(e.compareDocumentPosition(t)&16):!1:!1}function G1(e){e=e!=null&&e.ownerDocument!=null&&e.ownerDocument.defaultView!=null?e.ownerDocument.defaultView:window;for(var t=us(e.document);t instanceof e.HTMLIFrameElement;){try{var n=typeof t.contentWindow.location.href=="string"}catch{n=!1}if(n)e=t.contentWindow;else break;t=us(e.document)}return t}function Tr(e){var t=e&&e.nodeName&&e.nodeName.toLowerCase();return t&&(t==="input"&&(e.type==="text"||e.type==="search"||e.type==="tel"||e.type==="url"||e.type==="password")||t==="textarea"||e.contentEditable==="true")}var Eh=Mn&&"documentMode"in document&&11>=document.documentMode,ra=null,Dc=null,bo=null,Bc=!1;function rf(e,t,n){var l=n.window===n?n.document:n.nodeType===9?n:n.ownerDocument;Bc||ra==null||ra!==us(l)||(l=ra,"selectionStart"in l&&Tr(l)?l={start:l.selectionStart,end:l.selectionEnd}:(l=(l.ownerDocument&&l.ownerDocument.defaultView||window).getSelection(),l={anchorNode:l.anchorNode,anchorOffset:l.anchorOffset,focusNode:l.focusNode,focusOffset:l.focusOffset}),bo&&Oo(bo,l)||(bo=l,l=Ts(Dc,"onSelect"),0<l.length&&(t=new Ds("onSelect","select",null,t,n),e.push({event:t,listeners:l}),t.target=ra)))}function vl(e,t){var n={};return n[e.toLowerCase()]=t.toLowerCase(),n["Webkit"+e]="webkit"+t,n["Moz"+e]="moz"+t,n}var da={animationend:vl("Animation","AnimationEnd"),animationiteration:vl("Animation","AnimationIteration"),animationstart:vl("Animation","AnimationStart"),transitionrun:vl("Transition","TransitionRun"),transitionstart:vl("Transition","TransitionStart"),transitioncancel:vl("Transition","TransitionCancel"),transitionend:vl("Transition","TransitionEnd")},Iu={},V1={};Mn&&(V1=document.createElement("div").style,"AnimationEvent"in window||(delete da.animationend.animation,delete da.animationiteration.animation,delete da.animationstart.animation),"TransitionEvent"in window||delete da.transitionend.transition);function Yl(e){if(Iu[e])return Iu[e];if(!da[e])return e;var t=da[e],n;for(n in t)if(t.hasOwnProperty(n)&&n in V1)return Iu[e]=t[n];return e}var K1=Yl("animationend"),J1=Yl("animationiteration"),W1=Yl("animationstart"),Th=Yl("transitionrun"),kh=Yl("transitionstart"),Mh=Yl("transitioncancel"),I1=Yl("transitionend"),F1=new Map,Hc="abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");Hc.push("scrollEnd");function Zt(e,t){F1.set(e,t),Bl(t,[e])}var cs=typeof reportError=="function"?reportError:function(e){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var t=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof e=="object"&&e!==null&&typeof e.message=="string"?String(e.message):String(e),error:e});if(!window.dispatchEvent(t))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",e);return}console.error(e)},Nt=[],_a=0,kr=0;function Ys(){for(var e=_a,t=kr=_a=0;t<e;){var n=Nt[t];Nt[t++]=null;var l=Nt[t];Nt[t++]=null;var a=Nt[t];Nt[t++]=null;var o=Nt[t];if(Nt[t++]=null,l!==null&&a!==null){var i=l.pending;i===null?a.next=a:(a.next=i.next,i.next=a),l.pending=a}o!==0&&P1(n,a,o)}}function Rs(e,t,n,l){Nt[_a++]=e,Nt[_a++]=t,Nt[_a++]=n,Nt[_a++]=l,kr|=l,e.lanes|=l,e=e.alternate,e!==null&&(e.lanes|=l)}function Mr(e,t,n,l){return Rs(e,t,n,l),rs(e)}function Rl(e,t){return Rs(e,null,null,t),rs(e)}function P1(e,t,n){e.lanes|=n;var l=e.alternate;l!==null&&(l.lanes|=n);for(var a=!1,o=e.return;o!==null;)o.childLanes|=n,l=o.alternate,l!==null&&(l.childLanes|=n),o.tag===22&&(e=o.stateNode,e===null||e._visibility&1||(a=!0)),e=o,o=o.return;return e.tag===3?(o=e.stateNode,a&&t!==null&&(a=31-Tt(n),e=o.hiddenUpdates,l=e[a],l===null?e[a]=[t]:l.push(t),t.lane=n|536870912),o):null}function rs(e){if(50<Mo)throw Mo=0,lr=null,Error(E(185));for(var t=e.return;t!==null;)e=t,t=e.return;return e.tag===3?e.stateNode:null}var fa={};function Ah(e,t,n,l){this.tag=e,this.key=n,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.refCleanup=this.ref=null,this.pendingProps=t,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=l,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function xt(e,t,n,l){return new Ah(e,t,n,l)}function Ar(e){return e=e.prototype,!(!e||!e.isReactComponent)}function En(e,t){var n=e.alternate;return n===null?(n=xt(e.tag,t,e.key,e.mode),n.elementType=e.elementType,n.type=e.type,n.stateNode=e.stateNode,n.alternate=e,e.alternate=n):(n.pendingProps=t,n.type=e.type,n.flags=0,n.subtreeFlags=0,n.deletions=null),n.flags=e.flags&65011712,n.childLanes=e.childLanes,n.lanes=e.lanes,n.child=e.child,n.memoizedProps=e.memoizedProps,n.memoizedState=e.memoizedState,n.updateQueue=e.updateQueue,t=e.dependencies,n.dependencies=t===null?null:{lanes:t.lanes,firstContext:t.firstContext},n.sibling=e.sibling,n.index=e.index,n.ref=e.ref,n.refCleanup=e.refCleanup,n}function e0(e,t){e.flags&=65011714;var n=e.alternate;return n===null?(e.childLanes=0,e.lanes=t,e.child=null,e.subtreeFlags=0,e.memoizedProps=null,e.memoizedState=null,e.updateQueue=null,e.dependencies=null,e.stateNode=null):(e.childLanes=n.childLanes,e.lanes=n.lanes,e.child=n.child,e.subtreeFlags=0,e.deletions=null,e.memoizedProps=n.memoizedProps,e.memoizedState=n.memoizedState,e.updateQueue=n.updateQueue,e.type=n.type,t=n.dependencies,e.dependencies=t===null?null:{lanes:t.lanes,firstContext:t.firstContext}),e}function Vi(e,t,n,l,a,o){var i=0;if(l=e,typeof e=="function")Ar(e)&&(i=1);else if(typeof e=="string")i=Ly(e,n,tn.current)?26:e==="html"||e==="head"||e==="body"?27:5;else e:switch(e){case Cc:return e=xt(31,n,t,a),e.elementType=Cc,e.lanes=o,e;case oa:return Tl(n.children,a,o,t);case b1:i=8,a|=24;break;case vc:return e=xt(12,n,t,a|2),e.elementType=vc,e.lanes=o,e;case Sc:return e=xt(13,n,t,a),e.elementType=Sc,e.lanes=o,e;case xc:return e=xt(19,n,t,a),e.elementType=xc,e.lanes=o,e;default:if(typeof e=="object"&&e!==null)switch(e.$$typeof){case xn:i=10;break e;case v1:i=9;break e;case hr:i=11;break e;case yr:i=14;break e;case jn:i=16,l=null;break e}i=29,n=Error(E(130,e===null?"null":typeof e,"")),l=null}return t=xt(i,n,t,a),t.elementType=e,t.type=l,t.lanes=o,t}function Tl(e,t,n,l){return e=xt(7,e,l,t),e.lanes=n,e}function Fu(e,t,n){return e=xt(6,e,null,t),e.lanes=n,e}function t0(e){var t=xt(18,null,null,0);return t.stateNode=e,t}function Pu(e,t,n){return t=xt(4,e.children!==null?e.children:[],e.key,t),t.lanes=n,t.stateNode={containerInfo:e.containerInfo,pendingChildren:null,implementation:e.implementation},t}var df=new WeakMap;function Ht(e,t){if(typeof e=="object"&&e!==null){var n=df.get(e);return n!==void 0?n:(t={value:e,source:t,stack:Z_(t)},df.set(e,t),t)}return{value:e,source:t,stack:Z_(t)}}var ma=[],ha=0,ds=null,Do=0,Ot=[],Dt=0,il=null,Ft=1,Pt="";function vn(e,t){ma[ha++]=Do,ma[ha++]=ds,ds=e,Do=t}function n0(e,t,n){Ot[Dt++]=Ft,Ot[Dt++]=Pt,Ot[Dt++]=il,il=e;var l=Ft;e=Pt;var a=32-Tt(l)-1;l&=~(1<<a),n+=1;var o=32-Tt(t)+a;if(30<o){var i=a-a%5;o=(l&(1<<i)-1).toString(32),l>>=i,a-=i,Ft=1<<32-Tt(t)+a|n<<a|l,Pt=o+e}else Ft=1<<o|n<<a|l,Pt=e}function zr(e){e.return!==null&&(vn(e,1),n0(e,1,0))}function Nr(e){for(;e===ds;)ds=ma[--ha],ma[ha]=null,Do=ma[--ha],ma[ha]=null;for(;e===il;)il=Ot[--Dt],Ot[Dt]=null,Pt=Ot[--Dt],Ot[Dt]=null,Ft=Ot[--Dt],Ot[Dt]=null}function l0(e,t){Ot[Dt++]=Ft,Ot[Dt++]=Pt,Ot[Dt++]=il,Ft=t.id,Pt=t.overflow,il=e}var Ie=null,Ce=null,ie=!1,Fn=null,Yt=!1,Yc=Error(E(519));function sl(e){var t=Error(E(418,1<arguments.length&&arguments[1]!==void 0&&arguments[1]?"text":"HTML",""));throw Bo(Ht(t,e)),Yc}function _f(e){var t=e.stateNode,n=e.type,l=e.memoizedProps;switch(t[We]=e,t[mt]=l,n){case"dialog":ee("cancel",t),ee("close",t);break;case"iframe":case"object":case"embed":ee("load",t);break;case"video":case"audio":for(n=0;n<Uo.length;n++)ee(Uo[n],t);break;case"source":ee("error",t);break;case"img":case"image":case"link":ee("error",t),ee("load",t);break;case"details":ee("toggle",t);break;case"input":ee("invalid",t),O1(t,l.value,l.defaultValue,l.checked,l.defaultChecked,l.type,l.name,!0);break;case"select":ee("invalid",t);break;case"textarea":ee("invalid",t),B1(t,l.value,l.defaultValue,l.children)}n=l.children,typeof n!="string"&&typeof n!="number"&&typeof n!="bigint"||t.textContent===""+n||l.suppressHydrationWarning===!0||Um(t.textContent,n)?(l.popover!=null&&(ee("beforetoggle",t),ee("toggle",t)),l.onScroll!=null&&ee("scroll",t),l.onScrollEnd!=null&&ee("scrollend",t),l.onClick!=null&&(t.onclick=Cn),t=!0):t=!1,t||sl(e,!0)}function ff(e){for(Ie=e.return;Ie;)switch(Ie.tag){case 5:case 31:case 13:Yt=!1;return;case 27:case 3:Yt=!0;return;default:Ie=Ie.return}}function ta(e){if(e!==Ie)return!1;if(!ie)return ff(e),ie=!0,!1;var t=e.tag,n;if((n=t!==3&&t!==27)&&((n=t===5)&&(n=e.type,n=!(n!=="form"&&n!=="button")||ur(e.type,e.memoizedProps)),n=!n),n&&Ce&&sl(e),ff(e),t===13){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(E(317));Ce=t1(e)}else if(t===31){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(E(317));Ce=t1(e)}else t===27?(t=Ce,dl(e.type)?(e=_r,_r=null,Ce=e):Ce=t):Ce=Ie?Ut(e.stateNode.nextSibling):null;return!0}function zl(){Ce=Ie=null,ie=!1}function ec(){var e=Fn;return e!==null&&(_t===null?_t=e:_t.push.apply(_t,e),Fn=null),e}function Bo(e){Fn===null?Fn=[e]:Fn.push(e)}var Rc=nn(null),Ul=null,wn=null;function Qn(e,t,n){ve(Rc,t._currentValue),t._currentValue=n}function Tn(e){e._currentValue=Rc.current,Ke(Rc)}function Uc(e,t,n){for(;e!==null;){var l=e.alternate;if((e.childLanes&t)!==t?(e.childLanes|=t,l!==null&&(l.childLanes|=t)):l!==null&&(l.childLanes&t)!==t&&(l.childLanes|=t),e===n)break;e=e.return}}function jc(e,t,n,l){var a=e.child;for(a!==null&&(a.return=e);a!==null;){var o=a.dependencies;if(o!==null){var i=a.child;o=o.firstContext;e:for(;o!==null;){var s=o;o=a;for(var u=0;u<t.length;u++)if(s.context===t[u]){o.lanes|=n,s=o.alternate,s!==null&&(s.lanes|=n),Uc(o.return,n,e),l||(i=null);break e}o=s.next}}else if(a.tag===18){if(i=a.return,i===null)throw Error(E(341));i.lanes|=n,o=i.alternate,o!==null&&(o.lanes|=n),Uc(i,n,e),i=null}else i=a.child;if(i!==null)i.return=a;else for(i=a;i!==null;){if(i===e){i=null;break}if(a=i.sibling,a!==null){a.return=i.return,i=a;break}i=i.return}a=i}}function Ya(e,t,n,l){e=null;for(var a=t,o=!1;a!==null;){if(!o){if((a.flags&524288)!==0)o=!0;else if((a.flags&262144)!==0)break}if(a.tag===10){var i=a.alternate;if(i===null)throw Error(E(387));if(i=i.memoizedProps,i!==null){var s=a.type;Mt(a.pendingProps.value,i.value)||(e!==null?e.push(s):e=[s])}}else if(a===as.current){if(i=a.alternate,i===null)throw Error(E(387));i.memoizedState.memoizedState!==a.memoizedState.memoizedState&&(e!==null?e.push(Xo):e=[Xo])}a=a.return}e!==null&&jc(t,e,n,l),t.flags|=262144}function _s(e){for(e=e.firstContext;e!==null;){if(!Mt(e.context._currentValue,e.memoizedValue))return!0;e=e.next}return!1}function Nl(e){Ul=e,wn=null,e=e.dependencies,e!==null&&(e.firstContext=null)}function Fe(e){return a0(Ul,e)}function Oi(e,t){return Ul===null&&Nl(e),a0(e,t)}function a0(e,t){var n=t._currentValue;if(t={context:t,memoizedValue:n,next:null},wn===null){if(e===null)throw Error(E(308));wn=t,e.dependencies={lanes:0,firstContext:t},e.flags|=524288}else wn=wn.next=t;return n}var zh=typeof AbortController<"u"?AbortController:function(){var e=[],t=this.signal={aborted:!1,addEventListener:function(n,l){e.push(l)}};this.abort=function(){t.aborted=!0,e.forEach(function(n){return n()})}},Nh=$e.unstable_scheduleCallback,Lh=$e.unstable_NormalPriority,Xe={$$typeof:xn,Consumer:null,Provider:null,_currentValue:null,_currentValue2:null,_threadCount:0};function Lr(){return{controller:new zh,data:new Map,refCount:0}}function Wo(e){e.refCount--,e.refCount===0&&Nh(Lh,function(){e.controller.abort()})}var vo=null,Xc=0,ka=0,va=null;function Oh(e,t){if(vo===null){var n=vo=[];Xc=0,ka=ld(),va={status:"pending",value:void 0,then:function(l){n.push(l)}}}return Xc++,t.then(mf,mf),t}function mf(){if(--Xc===0&&vo!==null){va!==null&&(va.status="fulfilled");var e=vo;vo=null,ka=0,va=null;for(var t=0;t<e.length;t++)(0,e[t])()}}function Dh(e,t){var n=[],l={status:"pending",value:null,reason:null,then:function(a){n.push(a)}};return e.then(function(){l.status="fulfilled",l.value=t;for(var a=0;a<n.length;a++)(0,n[a])(t)},function(a){for(l.status="rejected",l.reason=a,a=0;a<n.length;a++)(0,n[a])(void 0)}),l}var hf=j.S;j.S=function(e,t){pm=wt(),typeof t=="object"&&t!==null&&typeof t.then=="function"&&Oh(e,t),hf!==null&&hf(e,t)};var kl=nn(null);function Or(){var e=kl.current;return e!==null?e:ge.pooledCache}function Ki(e,t){t===null?ve(kl,kl.current):ve(kl,t.pool)}function o0(){var e=Or();return e===null?null:{parent:Xe._currentValue,pool:e}}var Ra=Error(E(460)),Dr=Error(E(474)),Us=Error(E(542)),fs={then:function(){}};function yf(e){return e=e.status,e==="fulfilled"||e==="rejected"}function i0(e,t,n){switch(n=e[n],n===void 0?e.push(t):n!==t&&(t.then(Cn,Cn),t=n),t.status){case"fulfilled":return t.value;case"rejected":throw e=t.reason,pf(e),e;default:if(typeof t.status=="string")t.then(Cn,Cn);else{if(e=ge,e!==null&&100<e.shellSuspendCounter)throw Error(E(482));e=t,e.status="pending",e.then(function(l){if(t.status==="pending"){var a=t;a.status="fulfilled",a.value=l}},function(l){if(t.status==="pending"){var a=t;a.status="rejected",a.reason=l}})}switch(t.status){case"fulfilled":return t.value;case"rejected":throw e=t.reason,pf(e),e}throw Ml=t,Ra}}function Cl(e){try{var t=e._init;return t(e._payload)}catch(n){throw n!==null&&typeof n=="object"&&typeof n.then=="function"?(Ml=n,Ra):n}}var Ml=null;function gf(){if(Ml===null)throw Error(E(459));var e=Ml;return Ml=null,e}function pf(e){if(e===Ra||e===Us)throw Error(E(483))}var Sa=null,Ho=0;function Di(e){var t=Ho;return Ho+=1,Sa===null&&(Sa=[]),i0(Sa,e,t)}function io(e,t){t=t.props.ref,e.ref=t!==void 0?t:null}function Bi(e,t){throw t.$$typeof===v2?Error(E(525)):(e=Object.prototype.toString.call(t),Error(E(31,e==="[object Object]"?"object with keys {"+Object.keys(t).join(", ")+"}":e)))}function s0(e){function t(f,_){if(e){var g=f.deletions;g===null?(f.deletions=[_],f.flags|=16):g.push(_)}}function n(f,_){if(!e)return null;for(;_!==null;)t(f,_),_=_.sibling;return null}function l(f){for(var _=new Map;f!==null;)f.key!==null?_.set(f.key,f):_.set(f.index,f),f=f.sibling;return _}function a(f,_){return f=En(f,_),f.index=0,f.sibling=null,f}function o(f,_,g){return f.index=g,e?(g=f.alternate,g!==null?(g=g.index,g<_?(f.flags|=67108866,_):g):(f.flags|=67108866,_)):(f.flags|=1048576,_)}function i(f){return e&&f.alternate===null&&(f.flags|=67108866),f}function s(f,_,g,x){return _===null||_.tag!==6?(_=Fu(g,f.mode,x),_.return=f,_):(_=a(_,g),_.return=f,_)}function u(f,_,g,x){var O=g.type;return O===oa?y(f,_,g.props.children,x,g.key):_!==null&&(_.elementType===O||typeof O=="object"&&O!==null&&O.$$typeof===jn&&Cl(O)===_.type)?(_=a(_,g.props),io(_,g),_.return=f,_):(_=Vi(g.type,g.key,g.props,null,f.mode,x),io(_,g),_.return=f,_)}function h(f,_,g,x){return _===null||_.tag!==4||_.stateNode.containerInfo!==g.containerInfo||_.stateNode.implementation!==g.implementation?(_=Pu(g,f.mode,x),_.return=f,_):(_=a(_,g.children||[]),_.return=f,_)}function y(f,_,g,x,O){return _===null||_.tag!==7?(_=Tl(g,f.mode,x,O),_.return=f,_):(_=a(_,g),_.return=f,_)}function S(f,_,g){if(typeof _=="string"&&_!==""||typeof _=="number"||typeof _=="bigint")return _=Fu(""+_,f.mode,g),_.return=f,_;if(typeof _=="object"&&_!==null){switch(_.$$typeof){case Ei:return g=Vi(_.type,_.key,_.props,null,f.mode,g),io(g,_),g.return=f,g;case _o:return _=Pu(_,f.mode,g),_.return=f,_;case jn:return _=Cl(_),S(f,_,g)}if(fo(_)||ao(_))return _=Tl(_,f.mode,g,null),_.return=f,_;if(typeof _.then=="function")return S(f,Di(_),g);if(_.$$typeof===xn)return S(f,Oi(f,_),g);Bi(f,_)}return null}function p(f,_,g,x){var O=_!==null?_.key:null;if(typeof g=="string"&&g!==""||typeof g=="number"||typeof g=="bigint")return O!==null?null:s(f,_,""+g,x);if(typeof g=="object"&&g!==null){switch(g.$$typeof){case Ei:return g.key===O?u(f,_,g,x):null;case _o:return g.key===O?h(f,_,g,x):null;case jn:return g=Cl(g),p(f,_,g,x)}if(fo(g)||ao(g))return O!==null?null:y(f,_,g,x,null);if(typeof g.then=="function")return p(f,_,Di(g),x);if(g.$$typeof===xn)return p(f,_,Oi(f,g),x);Bi(f,g)}return null}function b(f,_,g,x,O){if(typeof x=="string"&&x!==""||typeof x=="number"||typeof x=="bigint")return f=f.get(g)||null,s(_,f,""+x,O);if(typeof x=="object"&&x!==null){switch(x.$$typeof){case Ei:return f=f.get(x.key===null?g:x.key)||null,u(_,f,x,O);case _o:return f=f.get(x.key===null?g:x.key)||null,h(_,f,x,O);case jn:return x=Cl(x),b(f,_,g,x,O)}if(fo(x)||ao(x))return f=f.get(g)||null,y(_,f,x,O,null);if(typeof x.then=="function")return b(f,_,g,Di(x),O);if(x.$$typeof===xn)return b(f,_,g,Oi(_,x),O);Bi(_,x)}return null}function A(f,_,g,x){for(var O=null,le=null,L=_,U=_=0,W=null;L!==null&&U<g.length;U++){L.index>U?(W=L,L=null):W=L.sibling;var $=p(f,L,g[U],x);if($===null){L===null&&(L=W);break}e&&L&&$.alternate===null&&t(f,L),_=o($,_,U),le===null?O=$:le.sibling=$,le=$,L=W}if(U===g.length)return n(f,L),ie&&vn(f,U),O;if(L===null){for(;U<g.length;U++)L=S(f,g[U],x),L!==null&&(_=o(L,_,U),le===null?O=L:le.sibling=L,le=L);return ie&&vn(f,U),O}for(L=l(L);U<g.length;U++)W=b(L,f,U,g[U],x),W!==null&&(e&&W.alternate!==null&&L.delete(W.key===null?U:W.key),_=o(W,_,U),le===null?O=W:le.sibling=W,le=W);return e&&L.forEach(function(gt){return t(f,gt)}),ie&&vn(f,U),O}function k(f,_,g,x){if(g==null)throw Error(E(151));for(var O=null,le=null,L=_,U=_=0,W=null,$=g.next();L!==null&&!$.done;U++,$=g.next()){L.index>U?(W=L,L=null):W=L.sibling;var gt=p(f,L,$.value,x);if(gt===null){L===null&&(L=W);break}e&&L&&gt.alternate===null&&t(f,L),_=o(gt,_,U),le===null?O=gt:le.sibling=gt,le=gt,L=W}if($.done)return n(f,L),ie&&vn(f,U),O;if(L===null){for(;!$.done;U++,$=g.next())$=S(f,$.value,x),$!==null&&(_=o($,_,U),le===null?O=$:le.sibling=$,le=$);return ie&&vn(f,U),O}for(L=l(L);!$.done;U++,$=g.next())$=b(L,f,U,$.value,x),$!==null&&(e&&$.alternate!==null&&L.delete($.key===null?U:$.key),_=o($,_,U),le===null?O=$:le.sibling=$,le=$);return e&&L.forEach(function(Be){return t(f,Be)}),ie&&vn(f,U),O}function G(f,_,g,x){if(typeof g=="object"&&g!==null&&g.type===oa&&g.key===null&&(g=g.props.children),typeof g=="object"&&g!==null){switch(g.$$typeof){case Ei:e:{for(var O=g.key;_!==null;){if(_.key===O){if(O=g.type,O===oa){if(_.tag===7){n(f,_.sibling),x=a(_,g.props.children),x.return=f,f=x;break e}}else if(_.elementType===O||typeof O=="object"&&O!==null&&O.$$typeof===jn&&Cl(O)===_.type){n(f,_.sibling),x=a(_,g.props),io(x,g),x.return=f,f=x;break e}n(f,_);break}else t(f,_);_=_.sibling}g.type===oa?(x=Tl(g.props.children,f.mode,x,g.key),x.return=f,f=x):(x=Vi(g.type,g.key,g.props,null,f.mode,x),io(x,g),x.return=f,f=x)}return i(f);case _o:e:{for(O=g.key;_!==null;){if(_.key===O)if(_.tag===4&&_.stateNode.containerInfo===g.containerInfo&&_.stateNode.implementation===g.implementation){n(f,_.sibling),x=a(_,g.children||[]),x.return=f,f=x;break e}else{n(f,_);break}else t(f,_);_=_.sibling}x=Pu(g,f.mode,x),x.return=f,f=x}return i(f);case jn:return g=Cl(g),G(f,_,g,x)}if(fo(g))return A(f,_,g,x);if(ao(g)){if(O=ao(g),typeof O!="function")throw Error(E(150));return g=O.call(g),k(f,_,g,x)}if(typeof g.then=="function")return G(f,_,Di(g),x);if(g.$$typeof===xn)return G(f,_,Oi(f,g),x);Bi(f,g)}return typeof g=="string"&&g!==""||typeof g=="number"||typeof g=="bigint"?(g=""+g,_!==null&&_.tag===6?(n(f,_.sibling),x=a(_,g),x.return=f,f=x):(n(f,_),x=Fu(g,f.mode,x),x.return=f,f=x),i(f)):n(f,_)}return function(f,_,g,x){try{Ho=0;var O=G(f,_,g,x);return Sa=null,O}catch(L){if(L===Ra||L===Us)throw L;var le=xt(29,L,null,f.mode);return le.lanes=x,le.return=f,le}}}var Ll=s0(!0),u0=s0(!1),Xn=!1;function Br(e){e.updateQueue={baseState:e.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,lanes:0,hiddenCallbacks:null},callbacks:null}}function Qc(e,t){e=e.updateQueue,t.updateQueue===e&&(t.updateQueue={baseState:e.baseState,firstBaseUpdate:e.firstBaseUpdate,lastBaseUpdate:e.lastBaseUpdate,shared:e.shared,callbacks:null})}function Pn(e){return{lane:e,tag:0,payload:null,callback:null,next:null}}function el(e,t,n){var l=e.updateQueue;if(l===null)return null;if(l=l.shared,(ue&2)!==0){var a=l.pending;return a===null?t.next=t:(t.next=a.next,a.next=t),l.pending=t,t=rs(e),P1(e,null,n),t}return Rs(e,l,t,n),rs(e)}function So(e,t,n){if(t=t.updateQueue,t!==null&&(t=t.shared,(n&4194048)!==0)){var l=t.lanes;l&=e.pendingLanes,n|=l,t.lanes=n,T1(e,n)}}function tc(e,t){var n=e.updateQueue,l=e.alternate;if(l!==null&&(l=l.updateQueue,n===l)){var a=null,o=null;if(n=n.firstBaseUpdate,n!==null){do{var i={lane:n.lane,tag:n.tag,payload:n.payload,callback:null,next:null};o===null?a=o=i:o=o.next=i,n=n.next}while(n!==null);o===null?a=o=t:o=o.next=t}else a=o=t;n={baseState:l.baseState,firstBaseUpdate:a,lastBaseUpdate:o,shared:l.shared,callbacks:l.callbacks},e.updateQueue=n;return}e=n.lastBaseUpdate,e===null?n.firstBaseUpdate=t:e.next=t,n.lastBaseUpdate=t}var qc=!1;function xo(){if(qc){var e=va;if(e!==null)throw e}}function Co(e,t,n,l){qc=!1;var a=e.updateQueue;Xn=!1;var o=a.firstBaseUpdate,i=a.lastBaseUpdate,s=a.shared.pending;if(s!==null){a.shared.pending=null;var u=s,h=u.next;u.next=null,i===null?o=h:i.next=h,i=u;var y=e.alternate;y!==null&&(y=y.updateQueue,s=y.lastBaseUpdate,s!==i&&(s===null?y.firstBaseUpdate=h:s.next=h,y.lastBaseUpdate=u))}if(o!==null){var S=a.baseState;i=0,y=h=u=null,s=o;do{var p=s.lane&-536870913,b=p!==s.lane;if(b?(ae&p)===p:(l&p)===p){p!==0&&p===ka&&(qc=!0),y!==null&&(y=y.next={lane:0,tag:s.tag,payload:s.payload,callback:null,next:null});e:{var A=e,k=s;p=t;var G=n;switch(k.tag){case 1:if(A=k.payload,typeof A=="function"){S=A.call(G,S,p);break e}S=A;break e;case 3:A.flags=A.flags&-65537|128;case 0:if(A=k.payload,p=typeof A=="function"?A.call(G,S,p):A,p==null)break e;S=we({},S,p);break e;case 2:Xn=!0}}p=s.callback,p!==null&&(e.flags|=64,b&&(e.flags|=8192),b=a.callbacks,b===null?a.callbacks=[p]:b.push(p))}else b={lane:p,tag:s.tag,payload:s.payload,callback:s.callback,next:null},y===null?(h=y=b,u=S):y=y.next=b,i|=p;if(s=s.next,s===null){if(s=a.shared.pending,s===null)break;b=s,s=b.next,b.next=null,a.lastBaseUpdate=b,a.shared.pending=null}}while(!0);y===null&&(u=S),a.baseState=u,a.firstBaseUpdate=h,a.lastBaseUpdate=y,o===null&&(a.shared.lanes=0),cl|=i,e.lanes=i,e.memoizedState=S}}function c0(e,t){if(typeof e!="function")throw Error(E(191,e));e.call(t)}function r0(e,t){var n=e.callbacks;if(n!==null)for(e.callbacks=null,e=0;e<n.length;e++)c0(n[e],t)}var Ma=nn(null),ms=nn(0);function bf(e,t){e=Ln,ve(ms,e),ve(Ma,t),Ln=e|t.baseLanes}function $c(){ve(ms,Ln),ve(Ma,Ma.current)}function Hr(){Ln=ms.current,Ke(Ma),Ke(ms)}var At=nn(null),Rt=null;function qn(e){var t=e.alternate;ve(Oe,Oe.current&1),ve(At,e),Rt===null&&(t===null||Ma.current!==null||t.memoizedState!==null)&&(Rt=e)}function Zc(e){ve(Oe,Oe.current),ve(At,e),Rt===null&&(Rt=e)}function d0(e){e.tag===22?(ve(Oe,Oe.current),ve(At,e),Rt===null&&(Rt=e)):$n(e)}function $n(){ve(Oe,Oe.current),ve(At,At.current)}function St(e){Ke(At),Rt===e&&(Rt=null),Ke(Oe)}var Oe=nn(0);function hs(e){for(var t=e;t!==null;){if(t.tag===13){var n=t.memoizedState;if(n!==null&&(n=n.dehydrated,n===null||rr(n)||dr(n)))return t}else if(t.tag===19&&(t.memoizedProps.revealOrder==="forwards"||t.memoizedProps.revealOrder==="backwards"||t.memoizedProps.revealOrder==="unstable_legacy-backwards"||t.memoizedProps.revealOrder==="together")){if((t.flags&128)!==0)return t}else if(t.child!==null){t.child.return=t,t=t.child;continue}if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return null;t=t.return}t.sibling.return=t.return,t=t.sibling}return null}var An=0,J=null,me=null,Ue=null,ys=!1,xa=!1,Ol=!1,gs=0,Yo=0,Ca=null,Bh=0;function ze(){throw Error(E(321))}function Yr(e,t){if(t===null)return!1;for(var n=0;n<t.length&&n<e.length;n++)if(!Mt(e[n],t[n]))return!1;return!0}function Rr(e,t,n,l,a,o){return An=o,J=t,t.memoizedState=null,t.updateQueue=null,t.lanes=0,j.H=e===null||e.memoizedState===null?Q0:Jr,Ol=!1,o=n(l,a),Ol=!1,xa&&(o=f0(t,n,l,a)),_0(e),o}function _0(e){j.H=Ro;var t=me!==null&&me.next!==null;if(An=0,Ue=me=J=null,ys=!1,Yo=0,Ca=null,t)throw Error(E(300));e===null||Qe||(e=e.dependencies,e!==null&&_s(e)&&(Qe=!0))}function f0(e,t,n,l){J=e;var a=0;do{if(xa&&(Ca=null),Yo=0,xa=!1,25<=a)throw Error(E(301));if(a+=1,Ue=me=null,e.updateQueue!=null){var o=e.updateQueue;o.lastEffect=null,o.events=null,o.stores=null,o.memoCache!=null&&(o.memoCache.index=0)}j.H=q0,o=t(n,l)}while(xa);return o}function Hh(){var e=j.H,t=e.useState()[0];return t=typeof t.then=="function"?Io(t):t,e=e.useState()[0],(me!==null?me.memoizedState:null)!==e&&(J.flags|=1024),t}function Ur(){var e=gs!==0;return gs=0,e}function jr(e,t,n){t.updateQueue=e.updateQueue,t.flags&=-2053,e.lanes&=~n}function Xr(e){if(ys){for(e=e.memoizedState;e!==null;){var t=e.queue;t!==null&&(t.pending=null),e=e.next}ys=!1}An=0,Ue=me=J=null,xa=!1,Yo=gs=0,Ca=null}function it(){var e={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return Ue===null?J.memoizedState=Ue=e:Ue=Ue.next=e,Ue}function De(){if(me===null){var e=J.alternate;e=e!==null?e.memoizedState:null}else e=me.next;var t=Ue===null?J.memoizedState:Ue.next;if(t!==null)Ue=t,me=e;else{if(e===null)throw J.alternate===null?Error(E(467)):Error(E(310));me=e,e={memoizedState:me.memoizedState,baseState:me.baseState,baseQueue:me.baseQueue,queue:me.queue,next:null},Ue===null?J.memoizedState=Ue=e:Ue=Ue.next=e}return Ue}function js(){return{lastEffect:null,events:null,stores:null,memoCache:null}}function Io(e){var t=Yo;return Yo+=1,Ca===null&&(Ca=[]),e=i0(Ca,e,t),t=J,(Ue===null?t.memoizedState:Ue.next)===null&&(t=t.alternate,j.H=t===null||t.memoizedState===null?Q0:Jr),e}function Xs(e){if(e!==null&&typeof e=="object"){if(typeof e.then=="function")return Io(e);if(e.$$typeof===xn)return Fe(e)}throw Error(E(438,String(e)))}function Qr(e){var t=null,n=J.updateQueue;if(n!==null&&(t=n.memoCache),t==null){var l=J.alternate;l!==null&&(l=l.updateQueue,l!==null&&(l=l.memoCache,l!=null&&(t={data:l.data.map(function(a){return a.slice()}),index:0})))}if(t==null&&(t={data:[],index:0}),n===null&&(n=js(),J.updateQueue=n),n.memoCache=t,n=t.data[t.index],n===void 0)for(n=t.data[t.index]=Array(e),l=0;l<e;l++)n[l]=S2;return t.index++,n}function zn(e,t){return typeof t=="function"?t(e):t}function Ji(e){var t=De();return qr(t,me,e)}function qr(e,t,n){var l=e.queue;if(l===null)throw Error(E(311));l.lastRenderedReducer=n;var a=e.baseQueue,o=l.pending;if(o!==null){if(a!==null){var i=a.next;a.next=o.next,o.next=i}t.baseQueue=a=o,l.pending=null}if(o=e.baseState,a===null)e.memoizedState=o;else{t=a.next;var s=i=null,u=null,h=t,y=!1;do{var S=h.lane&-536870913;if(S!==h.lane?(ae&S)===S:(An&S)===S){var p=h.revertLane;if(p===0)u!==null&&(u=u.next={lane:0,revertLane:0,gesture:null,action:h.action,hasEagerState:h.hasEagerState,eagerState:h.eagerState,next:null}),S===ka&&(y=!0);else if((An&p)===p){h=h.next,p===ka&&(y=!0);continue}else S={lane:0,revertLane:h.revertLane,gesture:null,action:h.action,hasEagerState:h.hasEagerState,eagerState:h.eagerState,next:null},u===null?(s=u=S,i=o):u=u.next=S,J.lanes|=p,cl|=p;S=h.action,Ol&&n(o,S),o=h.hasEagerState?h.eagerState:n(o,S)}else p={lane:S,revertLane:h.revertLane,gesture:h.gesture,action:h.action,hasEagerState:h.hasEagerState,eagerState:h.eagerState,next:null},u===null?(s=u=p,i=o):u=u.next=p,J.lanes|=S,cl|=S;h=h.next}while(h!==null&&h!==t);if(u===null?i=o:u.next=s,!Mt(o,e.memoizedState)&&(Qe=!0,y&&(n=va,n!==null)))throw n;e.memoizedState=o,e.baseState=i,e.baseQueue=u,l.lastRenderedState=o}return a===null&&(l.lanes=0),[e.memoizedState,l.dispatch]}function nc(e){var t=De(),n=t.queue;if(n===null)throw Error(E(311));n.lastRenderedReducer=e;var l=n.dispatch,a=n.pending,o=t.memoizedState;if(a!==null){n.pending=null;var i=a=a.next;do o=e(o,i.action),i=i.next;while(i!==a);Mt(o,t.memoizedState)||(Qe=!0),t.memoizedState=o,t.baseQueue===null&&(t.baseState=o),n.lastRenderedState=o}return[o,l]}function m0(e,t,n){var l=J,a=De(),o=ie;if(o){if(n===void 0)throw Error(E(407));n=n()}else n=t();var i=!Mt((me||a).memoizedState,n);if(i&&(a.memoizedState=n,Qe=!0),a=a.queue,$r(g0.bind(null,l,a,e),[e]),a.getSnapshot!==t||i||Ue!==null&&Ue.memoizedState.tag&1){if(l.flags|=2048,Aa(9,{destroy:void 0},y0.bind(null,l,a,n,t),null),ge===null)throw Error(E(349));o||(An&127)!==0||h0(l,t,n)}return n}function h0(e,t,n){e.flags|=16384,e={getSnapshot:t,value:n},t=J.updateQueue,t===null?(t=js(),J.updateQueue=t,t.stores=[e]):(n=t.stores,n===null?t.stores=[e]:n.push(e))}function y0(e,t,n,l){t.value=n,t.getSnapshot=l,p0(t)&&b0(e)}function g0(e,t,n){return n(function(){p0(t)&&b0(e)})}function p0(e){var t=e.getSnapshot;e=e.value;try{var n=t();return!Mt(e,n)}catch{return!0}}function b0(e){var t=Rl(e,2);t!==null&&ft(t,e,2)}function Gc(e){var t=it();if(typeof e=="function"){var n=e;if(e=n(),Ol){Gn(!0);try{n()}finally{Gn(!1)}}}return t.memoizedState=t.baseState=e,t.queue={pending:null,lanes:0,dispatch:null,lastRenderedReducer:zn,lastRenderedState:e},t}function v0(e,t,n,l){return e.baseState=n,qr(e,me,typeof l=="function"?l:zn)}function Yh(e,t,n,l,a){if(qs(e))throw Error(E(485));if(e=t.action,e!==null){var o={payload:a,action:e,next:null,isTransition:!0,status:"pending",value:null,reason:null,listeners:[],then:function(i){o.listeners.push(i)}};j.T!==null?n(!0):o.isTransition=!1,l(o),n=t.pending,n===null?(o.next=t.pending=o,S0(t,o)):(o.next=n.next,t.pending=n.next=o)}}function S0(e,t){var n=t.action,l=t.payload,a=e.state;if(t.isTransition){var o=j.T,i={};j.T=i;try{var s=n(a,l),u=j.S;u!==null&&u(i,s),vf(e,t,s)}catch(h){Vc(e,t,h)}finally{o!==null&&i.types!==null&&(o.types=i.types),j.T=o}}else try{o=n(a,l),vf(e,t,o)}catch(h){Vc(e,t,h)}}function vf(e,t,n){n!==null&&typeof n=="object"&&typeof n.then=="function"?n.then(function(l){Sf(e,t,l)},function(l){return Vc(e,t,l)}):Sf(e,t,n)}function Sf(e,t,n){t.status="fulfilled",t.value=n,x0(t),e.state=n,t=e.pending,t!==null&&(n=t.next,n===t?e.pending=null:(n=n.next,t.next=n,S0(e,n)))}function Vc(e,t,n){var l=e.pending;if(e.pending=null,l!==null){l=l.next;do t.status="rejected",t.reason=n,x0(t),t=t.next;while(t!==l)}e.action=null}function x0(e){e=e.listeners;for(var t=0;t<e.length;t++)(0,e[t])()}function C0(e,t){return t}function xf(e,t){if(ie){var n=ge.formState;if(n!==null){e:{var l=J;if(ie){if(Ce){t:{for(var a=Ce,o=Yt;a.nodeType!==8;){if(!o){a=null;break t}if(a=Ut(a.nextSibling),a===null){a=null;break t}}o=a.data,a=o==="F!"||o==="F"?a:null}if(a){Ce=Ut(a.nextSibling),l=a.data==="F!";break e}}sl(l)}l=!1}l&&(t=n[0])}}return n=it(),n.memoizedState=n.baseState=t,l={pending:null,lanes:0,dispatch:null,lastRenderedReducer:C0,lastRenderedState:t},n.queue=l,n=U0.bind(null,J,l),l.dispatch=n,l=Gc(!1),o=Kr.bind(null,J,!1,l.queue),l=it(),a={state:t,dispatch:null,action:e,pending:null},l.queue=a,n=Yh.bind(null,J,a,o,n),a.dispatch=n,l.memoizedState=e,[t,n,!1]}function Cf(e){var t=De();return w0(t,me,e)}function w0(e,t,n){if(t=qr(e,t,C0)[0],e=Ji(zn)[0],typeof t=="object"&&t!==null&&typeof t.then=="function")try{var l=Io(t)}catch(i){throw i===Ra?Us:i}else l=t;t=De();var a=t.queue,o=a.dispatch;return n!==t.memoizedState&&(J.flags|=2048,Aa(9,{destroy:void 0},Rh.bind(null,a,n),null)),[l,o,e]}function Rh(e,t){e.action=t}function wf(e){var t=De(),n=me;if(n!==null)return w0(t,n,e);De(),t=t.memoizedState,n=De();var l=n.queue.dispatch;return n.memoizedState=e,[t,l,!1]}function Aa(e,t,n,l){return e={tag:e,create:n,deps:l,inst:t,next:null},t=J.updateQueue,t===null&&(t=js(),J.updateQueue=t),n=t.lastEffect,n===null?t.lastEffect=e.next=e:(l=n.next,n.next=e,e.next=l,t.lastEffect=e),e}function E0(){return De().memoizedState}function Wi(e,t,n,l){var a=it();J.flags|=e,a.memoizedState=Aa(1|t,{destroy:void 0},n,l===void 0?null:l)}function Qs(e,t,n,l){var a=De();l=l===void 0?null:l;var o=a.memoizedState.inst;me!==null&&l!==null&&Yr(l,me.memoizedState.deps)?a.memoizedState=Aa(t,o,n,l):(J.flags|=e,a.memoizedState=Aa(1|t,o,n,l))}function Ef(e,t){Wi(8390656,8,e,t)}function $r(e,t){Qs(2048,8,e,t)}function Uh(e){J.flags|=4;var t=J.updateQueue;if(t===null)t=js(),J.updateQueue=t,t.events=[e];else{var n=t.events;n===null?t.events=[e]:n.push(e)}}function T0(e){var t=De().memoizedState;return Uh({ref:t,nextImpl:e}),function(){if((ue&2)!==0)throw Error(E(440));return t.impl.apply(void 0,arguments)}}function k0(e,t){return Qs(4,2,e,t)}function M0(e,t){return Qs(4,4,e,t)}function A0(e,t){if(typeof t=="function"){e=e();var n=t(e);return function(){typeof n=="function"?n():t(null)}}if(t!=null)return e=e(),t.current=e,function(){t.current=null}}function z0(e,t,n){n=n!=null?n.concat([e]):null,Qs(4,4,A0.bind(null,t,e),n)}function Zr(){}function N0(e,t){var n=De();t=t===void 0?null:t;var l=n.memoizedState;return t!==null&&Yr(t,l[1])?l[0]:(n.memoizedState=[e,t],e)}function L0(e,t){var n=De();t=t===void 0?null:t;var l=n.memoizedState;if(t!==null&&Yr(t,l[1]))return l[0];if(l=e(),Ol){Gn(!0);try{e()}finally{Gn(!1)}}return n.memoizedState=[l,t],l}function Gr(e,t,n){return n===void 0||(An&1073741824)!==0&&(ae&261930)===0?e.memoizedState=t:(e.memoizedState=n,e=vm(),J.lanes|=e,cl|=e,n)}function O0(e,t,n,l){return Mt(n,t)?n:Ma.current!==null?(e=Gr(e,n,l),Mt(e,t)||(Qe=!0),e):(An&42)===0||(An&1073741824)!==0&&(ae&261930)===0?(Qe=!0,e.memoizedState=n):(e=vm(),J.lanes|=e,cl|=e,t)}function D0(e,t,n,l,a){var o=ce.p;ce.p=o!==0&&8>o?o:8;var i=j.T,s={};j.T=s,Kr(e,!1,t,n);try{var u=a(),h=j.S;if(h!==null&&h(s,u),u!==null&&typeof u=="object"&&typeof u.then=="function"){var y=Dh(u,l);wo(e,t,y,kt(e))}else wo(e,t,l,kt(e))}catch(S){wo(e,t,{then:function(){},status:"rejected",reason:S},kt())}finally{ce.p=o,i!==null&&s.types!==null&&(i.types=s.types),j.T=i}}function jh(){}function Kc(e,t,n,l){if(e.tag!==5)throw Error(E(476));var a=B0(e).queue;D0(e,a,t,El,n===null?jh:function(){return H0(e),n(l)})}function B0(e){var t=e.memoizedState;if(t!==null)return t;t={memoizedState:El,baseState:El,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:zn,lastRenderedState:El},next:null};var n={};return t.next={memoizedState:n,baseState:n,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:zn,lastRenderedState:n},next:null},e.memoizedState=t,e=e.alternate,e!==null&&(e.memoizedState=t),t}function H0(e){var t=B0(e);t.next===null&&(t=e.alternate.memoizedState),wo(e,t.next.queue,{},kt())}function Vr(){return Fe(Xo)}function Y0(){return De().memoizedState}function R0(){return De().memoizedState}function Xh(e){for(var t=e.return;t!==null;){switch(t.tag){case 24:case 3:var n=kt();e=Pn(n);var l=el(t,e,n);l!==null&&(ft(l,t,n),So(l,t,n)),t={cache:Lr()},e.payload=t;return}t=t.return}}function Qh(e,t,n){var l=kt();n={lane:l,revertLane:0,gesture:null,action:n,hasEagerState:!1,eagerState:null,next:null},qs(e)?j0(t,n):(n=Mr(e,t,n,l),n!==null&&(ft(n,e,l),X0(n,t,l)))}function U0(e,t,n){var l=kt();wo(e,t,n,l)}function wo(e,t,n,l){var a={lane:l,revertLane:0,gesture:null,action:n,hasEagerState:!1,eagerState:null,next:null};if(qs(e))j0(t,a);else{var o=e.alternate;if(e.lanes===0&&(o===null||o.lanes===0)&&(o=t.lastRenderedReducer,o!==null))try{var i=t.lastRenderedState,s=o(i,n);if(a.hasEagerState=!0,a.eagerState=s,Mt(s,i))return Rs(e,t,a,0),ge===null&&Ys(),!1}catch{}if(n=Mr(e,t,a,l),n!==null)return ft(n,e,l),X0(n,t,l),!0}return!1}function Kr(e,t,n,l){if(l={lane:2,revertLane:ld(),gesture:null,action:l,hasEagerState:!1,eagerState:null,next:null},qs(e)){if(t)throw Error(E(479))}else t=Mr(e,n,l,2),t!==null&&ft(t,e,2)}function qs(e){var t=e.alternate;return e===J||t!==null&&t===J}function j0(e,t){xa=ys=!0;var n=e.pending;n===null?t.next=t:(t.next=n.next,n.next=t),e.pending=t}function X0(e,t,n){if((n&4194048)!==0){var l=t.lanes;l&=e.pendingLanes,n|=l,t.lanes=n,T1(e,n)}}var Ro={readContext:Fe,use:Xs,useCallback:ze,useContext:ze,useEffect:ze,useImperativeHandle:ze,useLayoutEffect:ze,useInsertionEffect:ze,useMemo:ze,useReducer:ze,useRef:ze,useState:ze,useDebugValue:ze,useDeferredValue:ze,useTransition:ze,useSyncExternalStore:ze,useId:ze,useHostTransitionStatus:ze,useFormState:ze,useActionState:ze,useOptimistic:ze,useMemoCache:ze,useCacheRefresh:ze};Ro.useEffectEvent=ze;var Q0={readContext:Fe,use:Xs,useCallback:function(e,t){return it().memoizedState=[e,t===void 0?null:t],e},useContext:Fe,useEffect:Ef,useImperativeHandle:function(e,t,n){n=n!=null?n.concat([e]):null,Wi(4194308,4,A0.bind(null,t,e),n)},useLayoutEffect:function(e,t){return Wi(4194308,4,e,t)},useInsertionEffect:function(e,t){Wi(4,2,e,t)},useMemo:function(e,t){var n=it();t=t===void 0?null:t;var l=e();if(Ol){Gn(!0);try{e()}finally{Gn(!1)}}return n.memoizedState=[l,t],l},useReducer:function(e,t,n){var l=it();if(n!==void 0){var a=n(t);if(Ol){Gn(!0);try{n(t)}finally{Gn(!1)}}}else a=t;return l.memoizedState=l.baseState=a,e={pending:null,lanes:0,dispatch:null,lastRenderedReducer:e,lastRenderedState:a},l.queue=e,e=e.dispatch=Qh.bind(null,J,e),[l.memoizedState,e]},useRef:function(e){var t=it();return e={current:e},t.memoizedState=e},useState:function(e){e=Gc(e);var t=e.queue,n=U0.bind(null,J,t);return t.dispatch=n,[e.memoizedState,n]},useDebugValue:Zr,useDeferredValue:function(e,t){var n=it();return Gr(n,e,t)},useTransition:function(){var e=Gc(!1);return e=D0.bind(null,J,e.queue,!0,!1),it().memoizedState=e,[!1,e]},useSyncExternalStore:function(e,t,n){var l=J,a=it();if(ie){if(n===void 0)throw Error(E(407));n=n()}else{if(n=t(),ge===null)throw Error(E(349));(ae&127)!==0||h0(l,t,n)}a.memoizedState=n;var o={value:n,getSnapshot:t};return a.queue=o,Ef(g0.bind(null,l,o,e),[e]),l.flags|=2048,Aa(9,{destroy:void 0},y0.bind(null,l,o,n,t),null),n},useId:function(){var e=it(),t=ge.identifierPrefix;if(ie){var n=Pt,l=Ft;n=(l&~(1<<32-Tt(l)-1)).toString(32)+n,t="_"+t+"R_"+n,n=gs++,0<n&&(t+="H"+n.toString(32)),t+="_"}else n=Bh++,t="_"+t+"r_"+n.toString(32)+"_";return e.memoizedState=t},useHostTransitionStatus:Vr,useFormState:xf,useActionState:xf,useOptimistic:function(e){var t=it();t.memoizedState=t.baseState=e;var n={pending:null,lanes:0,dispatch:null,lastRenderedReducer:null,lastRenderedState:null};return t.queue=n,t=Kr.bind(null,J,!0,n),n.dispatch=t,[e,t]},useMemoCache:Qr,useCacheRefresh:function(){return it().memoizedState=Xh.bind(null,J)},useEffectEvent:function(e){var t=it(),n={impl:e};return t.memoizedState=n,function(){if((ue&2)!==0)throw Error(E(440));return n.impl.apply(void 0,arguments)}}},Jr={readContext:Fe,use:Xs,useCallback:N0,useContext:Fe,useEffect:$r,useImperativeHandle:z0,useInsertionEffect:k0,useLayoutEffect:M0,useMemo:L0,useReducer:Ji,useRef:E0,useState:function(){return Ji(zn)},useDebugValue:Zr,useDeferredValue:function(e,t){var n=De();return O0(n,me.memoizedState,e,t)},useTransition:function(){var e=Ji(zn)[0],t=De().memoizedState;return[typeof e=="boolean"?e:Io(e),t]},useSyncExternalStore:m0,useId:Y0,useHostTransitionStatus:Vr,useFormState:Cf,useActionState:Cf,useOptimistic:function(e,t){var n=De();return v0(n,me,e,t)},useMemoCache:Qr,useCacheRefresh:R0};Jr.useEffectEvent=T0;var q0={readContext:Fe,use:Xs,useCallback:N0,useContext:Fe,useEffect:$r,useImperativeHandle:z0,useInsertionEffect:k0,useLayoutEffect:M0,useMemo:L0,useReducer:nc,useRef:E0,useState:function(){return nc(zn)},useDebugValue:Zr,useDeferredValue:function(e,t){var n=De();return me===null?Gr(n,e,t):O0(n,me.memoizedState,e,t)},useTransition:function(){var e=nc(zn)[0],t=De().memoizedState;return[typeof e=="boolean"?e:Io(e),t]},useSyncExternalStore:m0,useId:Y0,useHostTransitionStatus:Vr,useFormState:wf,useActionState:wf,useOptimistic:function(e,t){var n=De();return me!==null?v0(n,me,e,t):(n.baseState=e,[e,n.queue.dispatch])},useMemoCache:Qr,useCacheRefresh:R0};q0.useEffectEvent=T0;function lc(e,t,n,l){t=e.memoizedState,n=n(l,t),n=n==null?t:we({},t,n),e.memoizedState=n,e.lanes===0&&(e.updateQueue.baseState=n)}var Jc={enqueueSetState:function(e,t,n){e=e._reactInternals;var l=kt(),a=Pn(l);a.payload=t,n!=null&&(a.callback=n),t=el(e,a,l),t!==null&&(ft(t,e,l),So(t,e,l))},enqueueReplaceState:function(e,t,n){e=e._reactInternals;var l=kt(),a=Pn(l);a.tag=1,a.payload=t,n!=null&&(a.callback=n),t=el(e,a,l),t!==null&&(ft(t,e,l),So(t,e,l))},enqueueForceUpdate:function(e,t){e=e._reactInternals;var n=kt(),l=Pn(n);l.tag=2,t!=null&&(l.callback=t),t=el(e,l,n),t!==null&&(ft(t,e,n),So(t,e,n))}};function Tf(e,t,n,l,a,o,i){return e=e.stateNode,typeof e.shouldComponentUpdate=="function"?e.shouldComponentUpdate(l,o,i):t.prototype&&t.prototype.isPureReactComponent?!Oo(n,l)||!Oo(a,o):!0}function kf(e,t,n,l){e=t.state,typeof t.componentWillReceiveProps=="function"&&t.componentWillReceiveProps(n,l),typeof t.UNSAFE_componentWillReceiveProps=="function"&&t.UNSAFE_componentWillReceiveProps(n,l),t.state!==e&&Jc.enqueueReplaceState(t,t.state,null)}function Dl(e,t){var n=t;if("ref"in t){n={};for(var l in t)l!=="ref"&&(n[l]=t[l])}if(e=e.defaultProps){n===t&&(n=we({},n));for(var a in e)n[a]===void 0&&(n[a]=e[a])}return n}function $0(e){cs(e)}function Z0(e){console.error(e)}function G0(e){cs(e)}function ps(e,t){try{var n=e.onUncaughtError;n(t.value,{componentStack:t.stack})}catch(l){setTimeout(function(){throw l})}}function Mf(e,t,n){try{var l=e.onCaughtError;l(n.value,{componentStack:n.stack,errorBoundary:t.tag===1?t.stateNode:null})}catch(a){setTimeout(function(){throw a})}}function Wc(e,t,n){return n=Pn(n),n.tag=3,n.payload={element:null},n.callback=function(){ps(e,t)},n}function V0(e){return e=Pn(e),e.tag=3,e}function K0(e,t,n,l){var a=n.type.getDerivedStateFromError;if(typeof a=="function"){var o=l.value;e.payload=function(){return a(o)},e.callback=function(){Mf(t,n,l)}}var i=n.stateNode;i!==null&&typeof i.componentDidCatch=="function"&&(e.callback=function(){Mf(t,n,l),typeof a!="function"&&(tl===null?tl=new Set([this]):tl.add(this));var s=l.stack;this.componentDidCatch(l.value,{componentStack:s!==null?s:""})})}function qh(e,t,n,l,a){if(n.flags|=32768,l!==null&&typeof l=="object"&&typeof l.then=="function"){if(t=n.alternate,t!==null&&Ya(t,n,a,!0),n=At.current,n!==null){switch(n.tag){case 31:case 13:return Rt===null?Cs():n.alternate===null&&Ne===0&&(Ne=3),n.flags&=-257,n.flags|=65536,n.lanes=a,l===fs?n.flags|=16384:(t=n.updateQueue,t===null?n.updateQueue=new Set([l]):t.add(l),mc(e,l,a)),!1;case 22:return n.flags|=65536,l===fs?n.flags|=16384:(t=n.updateQueue,t===null?(t={transitions:null,markerInstances:null,retryQueue:new Set([l])},n.updateQueue=t):(n=t.retryQueue,n===null?t.retryQueue=new Set([l]):n.add(l)),mc(e,l,a)),!1}throw Error(E(435,n.tag))}return mc(e,l,a),Cs(),!1}if(ie)return t=At.current,t!==null?((t.flags&65536)===0&&(t.flags|=256),t.flags|=65536,t.lanes=a,l!==Yc&&(e=Error(E(422),{cause:l}),Bo(Ht(e,n)))):(l!==Yc&&(t=Error(E(423),{cause:l}),Bo(Ht(t,n))),e=e.current.alternate,e.flags|=65536,a&=-a,e.lanes|=a,l=Ht(l,n),a=Wc(e.stateNode,l,a),tc(e,a),Ne!==4&&(Ne=2)),!1;var o=Error(E(520),{cause:l});if(o=Ht(o,n),ko===null?ko=[o]:ko.push(o),Ne!==4&&(Ne=2),t===null)return!0;l=Ht(l,n),n=t;do{switch(n.tag){case 3:return n.flags|=65536,e=a&-a,n.lanes|=e,e=Wc(n.stateNode,l,e),tc(n,e),!1;case 1:if(t=n.type,o=n.stateNode,(n.flags&128)===0&&(typeof t.getDerivedStateFromError=="function"||o!==null&&typeof o.componentDidCatch=="function"&&(tl===null||!tl.has(o))))return n.flags|=65536,a&=-a,n.lanes|=a,a=V0(a),K0(a,e,n,l),tc(n,a),!1}n=n.return}while(n!==null);return!1}var Wr=Error(E(461)),Qe=!1;function Je(e,t,n,l){t.child=e===null?u0(t,null,n,l):Ll(t,e.child,n,l)}function Af(e,t,n,l,a){n=n.render;var o=t.ref;if("ref"in l){var i={};for(var s in l)s!=="ref"&&(i[s]=l[s])}else i=l;return Nl(t),l=Rr(e,t,n,i,o,a),s=Ur(),e!==null&&!Qe?(jr(e,t,a),Nn(e,t,a)):(ie&&s&&zr(t),t.flags|=1,Je(e,t,l,a),t.child)}function zf(e,t,n,l,a){if(e===null){var o=n.type;return typeof o=="function"&&!Ar(o)&&o.defaultProps===void 0&&n.compare===null?(t.tag=15,t.type=o,J0(e,t,o,l,a)):(e=Vi(n.type,null,l,t,t.mode,a),e.ref=t.ref,e.return=t,t.child=e)}if(o=e.child,!Ir(e,a)){var i=o.memoizedProps;if(n=n.compare,n=n!==null?n:Oo,n(i,l)&&e.ref===t.ref)return Nn(e,t,a)}return t.flags|=1,e=En(o,l),e.ref=t.ref,e.return=t,t.child=e}function J0(e,t,n,l,a){if(e!==null){var o=e.memoizedProps;if(Oo(o,l)&&e.ref===t.ref)if(Qe=!1,t.pendingProps=l=o,Ir(e,a))(e.flags&131072)!==0&&(Qe=!0);else return t.lanes=e.lanes,Nn(e,t,a)}return Ic(e,t,n,l,a)}function W0(e,t,n,l){var a=l.children,o=e!==null?e.memoizedState:null;if(e===null&&t.stateNode===null&&(t.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),l.mode==="hidden"){if((t.flags&128)!==0){if(o=o!==null?o.baseLanes|n:n,e!==null){for(l=t.child=e.child,a=0;l!==null;)a=a|l.lanes|l.childLanes,l=l.sibling;l=a&~o}else l=0,t.child=null;return Nf(e,t,o,n,l)}if((n&536870912)!==0)t.memoizedState={baseLanes:0,cachePool:null},e!==null&&Ki(t,o!==null?o.cachePool:null),o!==null?bf(t,o):$c(),d0(t);else return l=t.lanes=536870912,Nf(e,t,o!==null?o.baseLanes|n:n,n,l)}else o!==null?(Ki(t,o.cachePool),bf(t,o),$n(t),t.memoizedState=null):(e!==null&&Ki(t,null),$c(),$n(t));return Je(e,t,a,n),t.child}function ho(e,t){return e!==null&&e.tag===22||t.stateNode!==null||(t.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),t.sibling}function Nf(e,t,n,l,a){var o=Or();return o=o===null?null:{parent:Xe._currentValue,pool:o},t.memoizedState={baseLanes:n,cachePool:o},e!==null&&Ki(t,null),$c(),d0(t),e!==null&&Ya(e,t,l,!0),t.childLanes=a,null}function Ii(e,t){return t=bs({mode:t.mode,children:t.children},e.mode),t.ref=e.ref,e.child=t,t.return=e,t}function Lf(e,t,n){return Ll(t,e.child,null,n),e=Ii(t,t.pendingProps),e.flags|=2,St(t),t.memoizedState=null,e}function $h(e,t,n){var l=t.pendingProps,a=(t.flags&128)!==0;if(t.flags&=-129,e===null){if(ie){if(l.mode==="hidden")return e=Ii(t,l),t.lanes=536870912,ho(null,e);if(Zc(t),(e=Ce)?(e=Qm(e,Yt),e=e!==null&&e.data==="&"?e:null,e!==null&&(t.memoizedState={dehydrated:e,treeContext:il!==null?{id:Ft,overflow:Pt}:null,retryLane:536870912,hydrationErrors:null},n=t0(e),n.return=t,t.child=n,Ie=t,Ce=null)):e=null,e===null)throw sl(t);return t.lanes=536870912,null}return Ii(t,l)}var o=e.memoizedState;if(o!==null){var i=o.dehydrated;if(Zc(t),a)if(t.flags&256)t.flags&=-257,t=Lf(e,t,n);else if(t.memoizedState!==null)t.child=e.child,t.flags|=128,t=null;else throw Error(E(558));else if(Qe||Ya(e,t,n,!1),a=(n&e.childLanes)!==0,Qe||a){if(l=ge,l!==null&&(i=k1(l,n),i!==0&&i!==o.retryLane))throw o.retryLane=i,Rl(e,i),ft(l,e,i),Wr;Cs(),t=Lf(e,t,n)}else e=o.treeContext,Ce=Ut(i.nextSibling),Ie=t,ie=!0,Fn=null,Yt=!1,e!==null&&l0(t,e),t=Ii(t,l),t.flags|=4096;return t}return e=En(e.child,{mode:l.mode,children:l.children}),e.ref=t.ref,t.child=e,e.return=t,e}function Fi(e,t){var n=t.ref;if(n===null)e!==null&&e.ref!==null&&(t.flags|=4194816);else{if(typeof n!="function"&&typeof n!="object")throw Error(E(284));(e===null||e.ref!==n)&&(t.flags|=4194816)}}function Ic(e,t,n,l,a){return Nl(t),n=Rr(e,t,n,l,void 0,a),l=Ur(),e!==null&&!Qe?(jr(e,t,a),Nn(e,t,a)):(ie&&l&&zr(t),t.flags|=1,Je(e,t,n,a),t.child)}function Of(e,t,n,l,a,o){return Nl(t),t.updateQueue=null,n=f0(t,l,n,a),_0(e),l=Ur(),e!==null&&!Qe?(jr(e,t,o),Nn(e,t,o)):(ie&&l&&zr(t),t.flags|=1,Je(e,t,n,o),t.child)}function Df(e,t,n,l,a){if(Nl(t),t.stateNode===null){var o=fa,i=n.contextType;typeof i=="object"&&i!==null&&(o=Fe(i)),o=new n(l,o),t.memoizedState=o.state!==null&&o.state!==void 0?o.state:null,o.updater=Jc,t.stateNode=o,o._reactInternals=t,o=t.stateNode,o.props=l,o.state=t.memoizedState,o.refs={},Br(t),i=n.contextType,o.context=typeof i=="object"&&i!==null?Fe(i):fa,o.state=t.memoizedState,i=n.getDerivedStateFromProps,typeof i=="function"&&(lc(t,n,i,l),o.state=t.memoizedState),typeof n.getDerivedStateFromProps=="function"||typeof o.getSnapshotBeforeUpdate=="function"||typeof o.UNSAFE_componentWillMount!="function"&&typeof o.componentWillMount!="function"||(i=o.state,typeof o.componentWillMount=="function"&&o.componentWillMount(),typeof o.UNSAFE_componentWillMount=="function"&&o.UNSAFE_componentWillMount(),i!==o.state&&Jc.enqueueReplaceState(o,o.state,null),Co(t,l,o,a),xo(),o.state=t.memoizedState),typeof o.componentDidMount=="function"&&(t.flags|=4194308),l=!0}else if(e===null){o=t.stateNode;var s=t.memoizedProps,u=Dl(n,s);o.props=u;var h=o.context,y=n.contextType;i=fa,typeof y=="object"&&y!==null&&(i=Fe(y));var S=n.getDerivedStateFromProps;y=typeof S=="function"||typeof o.getSnapshotBeforeUpdate=="function",s=t.pendingProps!==s,y||typeof o.UNSAFE_componentWillReceiveProps!="function"&&typeof o.componentWillReceiveProps!="function"||(s||h!==i)&&kf(t,o,l,i),Xn=!1;var p=t.memoizedState;o.state=p,Co(t,l,o,a),xo(),h=t.memoizedState,s||p!==h||Xn?(typeof S=="function"&&(lc(t,n,S,l),h=t.memoizedState),(u=Xn||Tf(t,n,u,l,p,h,i))?(y||typeof o.UNSAFE_componentWillMount!="function"&&typeof o.componentWillMount!="function"||(typeof o.componentWillMount=="function"&&o.componentWillMount(),typeof o.UNSAFE_componentWillMount=="function"&&o.UNSAFE_componentWillMount()),typeof o.componentDidMount=="function"&&(t.flags|=4194308)):(typeof o.componentDidMount=="function"&&(t.flags|=4194308),t.memoizedProps=l,t.memoizedState=h),o.props=l,o.state=h,o.context=i,l=u):(typeof o.componentDidMount=="function"&&(t.flags|=4194308),l=!1)}else{o=t.stateNode,Qc(e,t),i=t.memoizedProps,y=Dl(n,i),o.props=y,S=t.pendingProps,p=o.context,h=n.contextType,u=fa,typeof h=="object"&&h!==null&&(u=Fe(h)),s=n.getDerivedStateFromProps,(h=typeof s=="function"||typeof o.getSnapshotBeforeUpdate=="function")||typeof o.UNSAFE_componentWillReceiveProps!="function"&&typeof o.componentWillReceiveProps!="function"||(i!==S||p!==u)&&kf(t,o,l,u),Xn=!1,p=t.memoizedState,o.state=p,Co(t,l,o,a),xo();var b=t.memoizedState;i!==S||p!==b||Xn||e!==null&&e.dependencies!==null&&_s(e.dependencies)?(typeof s=="function"&&(lc(t,n,s,l),b=t.memoizedState),(y=Xn||Tf(t,n,y,l,p,b,u)||e!==null&&e.dependencies!==null&&_s(e.dependencies))?(h||typeof o.UNSAFE_componentWillUpdate!="function"&&typeof o.componentWillUpdate!="function"||(typeof o.componentWillUpdate=="function"&&o.componentWillUpdate(l,b,u),typeof o.UNSAFE_componentWillUpdate=="function"&&o.UNSAFE_componentWillUpdate(l,b,u)),typeof o.componentDidUpdate=="function"&&(t.flags|=4),typeof o.getSnapshotBeforeUpdate=="function"&&(t.flags|=1024)):(typeof o.componentDidUpdate!="function"||i===e.memoizedProps&&p===e.memoizedState||(t.flags|=4),typeof o.getSnapshotBeforeUpdate!="function"||i===e.memoizedProps&&p===e.memoizedState||(t.flags|=1024),t.memoizedProps=l,t.memoizedState=b),o.props=l,o.state=b,o.context=u,l=y):(typeof o.componentDidUpdate!="function"||i===e.memoizedProps&&p===e.memoizedState||(t.flags|=4),typeof o.getSnapshotBeforeUpdate!="function"||i===e.memoizedProps&&p===e.memoizedState||(t.flags|=1024),l=!1)}return o=l,Fi(e,t),l=(t.flags&128)!==0,o||l?(o=t.stateNode,n=l&&typeof n.getDerivedStateFromError!="function"?null:o.render(),t.flags|=1,e!==null&&l?(t.child=Ll(t,e.child,null,a),t.child=Ll(t,null,n,a)):Je(e,t,n,a),t.memoizedState=o.state,e=t.child):e=Nn(e,t,a),e}function Bf(e,t,n,l){return zl(),t.flags|=256,Je(e,t,n,l),t.child}var ac={dehydrated:null,treeContext:null,retryLane:0,hydrationErrors:null};function oc(e){return{baseLanes:e,cachePool:o0()}}function ic(e,t,n){return e=e!==null?e.childLanes&~n:0,t&&(e|=Ct),e}function I0(e,t,n){var l=t.pendingProps,a=!1,o=(t.flags&128)!==0,i;if((i=o)||(i=e!==null&&e.memoizedState===null?!1:(Oe.current&2)!==0),i&&(a=!0,t.flags&=-129),i=(t.flags&32)!==0,t.flags&=-33,e===null){if(ie){if(a?qn(t):$n(t),(e=Ce)?(e=Qm(e,Yt),e=e!==null&&e.data!=="&"?e:null,e!==null&&(t.memoizedState={dehydrated:e,treeContext:il!==null?{id:Ft,overflow:Pt}:null,retryLane:536870912,hydrationErrors:null},n=t0(e),n.return=t,t.child=n,Ie=t,Ce=null)):e=null,e===null)throw sl(t);return dr(e)?t.lanes=32:t.lanes=536870912,null}var s=l.children;return l=l.fallback,a?($n(t),a=t.mode,s=bs({mode:"hidden",children:s},a),l=Tl(l,a,n,null),s.return=t,l.return=t,s.sibling=l,t.child=s,l=t.child,l.memoizedState=oc(n),l.childLanes=ic(e,i,n),t.memoizedState=ac,ho(null,l)):(qn(t),Fc(t,s))}var u=e.memoizedState;if(u!==null&&(s=u.dehydrated,s!==null)){if(o)t.flags&256?(qn(t),t.flags&=-257,t=sc(e,t,n)):t.memoizedState!==null?($n(t),t.child=e.child,t.flags|=128,t=null):($n(t),s=l.fallback,a=t.mode,l=bs({mode:"visible",children:l.children},a),s=Tl(s,a,n,null),s.flags|=2,l.return=t,s.return=t,l.sibling=s,t.child=l,Ll(t,e.child,null,n),l=t.child,l.memoizedState=oc(n),l.childLanes=ic(e,i,n),t.memoizedState=ac,t=ho(null,l));else if(qn(t),dr(s)){if(i=s.nextSibling&&s.nextSibling.dataset,i)var h=i.dgst;i=h,l=Error(E(419)),l.stack="",l.digest=i,Bo({value:l,source:null,stack:null}),t=sc(e,t,n)}else if(Qe||Ya(e,t,n,!1),i=(n&e.childLanes)!==0,Qe||i){if(i=ge,i!==null&&(l=k1(i,n),l!==0&&l!==u.retryLane))throw u.retryLane=l,Rl(e,l),ft(i,e,l),Wr;rr(s)||Cs(),t=sc(e,t,n)}else rr(s)?(t.flags|=192,t.child=e.child,t=null):(e=u.treeContext,Ce=Ut(s.nextSibling),Ie=t,ie=!0,Fn=null,Yt=!1,e!==null&&l0(t,e),t=Fc(t,l.children),t.flags|=4096);return t}return a?($n(t),s=l.fallback,a=t.mode,u=e.child,h=u.sibling,l=En(u,{mode:"hidden",children:l.children}),l.subtreeFlags=u.subtreeFlags&65011712,h!==null?s=En(h,s):(s=Tl(s,a,n,null),s.flags|=2),s.return=t,l.return=t,l.sibling=s,t.child=l,ho(null,l),l=t.child,s=e.child.memoizedState,s===null?s=oc(n):(a=s.cachePool,a!==null?(u=Xe._currentValue,a=a.parent!==u?{parent:u,pool:u}:a):a=o0(),s={baseLanes:s.baseLanes|n,cachePool:a}),l.memoizedState=s,l.childLanes=ic(e,i,n),t.memoizedState=ac,ho(e.child,l)):(qn(t),n=e.child,e=n.sibling,n=En(n,{mode:"visible",children:l.children}),n.return=t,n.sibling=null,e!==null&&(i=t.deletions,i===null?(t.deletions=[e],t.flags|=16):i.push(e)),t.child=n,t.memoizedState=null,n)}function Fc(e,t){return t=bs({mode:"visible",children:t},e.mode),t.return=e,e.child=t}function bs(e,t){return e=xt(22,e,null,t),e.lanes=0,e}function sc(e,t,n){return Ll(t,e.child,null,n),e=Fc(t,t.pendingProps.children),e.flags|=2,t.memoizedState=null,e}function Hf(e,t,n){e.lanes|=t;var l=e.alternate;l!==null&&(l.lanes|=t),Uc(e.return,t,n)}function uc(e,t,n,l,a,o){var i=e.memoizedState;i===null?e.memoizedState={isBackwards:t,rendering:null,renderingStartTime:0,last:l,tail:n,tailMode:a,treeForkCount:o}:(i.isBackwards=t,i.rendering=null,i.renderingStartTime=0,i.last=l,i.tail=n,i.tailMode=a,i.treeForkCount=o)}function F0(e,t,n){var l=t.pendingProps,a=l.revealOrder,o=l.tail;l=l.children;var i=Oe.current,s=(i&2)!==0;if(s?(i=i&1|2,t.flags|=128):i&=1,ve(Oe,i),Je(e,t,l,n),l=ie?Do:0,!s&&e!==null&&(e.flags&128)!==0)e:for(e=t.child;e!==null;){if(e.tag===13)e.memoizedState!==null&&Hf(e,n,t);else if(e.tag===19)Hf(e,n,t);else if(e.child!==null){e.child.return=e,e=e.child;continue}if(e===t)break e;for(;e.sibling===null;){if(e.return===null||e.return===t)break e;e=e.return}e.sibling.return=e.return,e=e.sibling}switch(a){case"forwards":for(n=t.child,a=null;n!==null;)e=n.alternate,e!==null&&hs(e)===null&&(a=n),n=n.sibling;n=a,n===null?(a=t.child,t.child=null):(a=n.sibling,n.sibling=null),uc(t,!1,a,n,o,l);break;case"backwards":case"unstable_legacy-backwards":for(n=null,a=t.child,t.child=null;a!==null;){if(e=a.alternate,e!==null&&hs(e)===null){t.child=a;break}e=a.sibling,a.sibling=n,n=a,a=e}uc(t,!0,n,null,o,l);break;case"together":uc(t,!1,null,null,void 0,l);break;default:t.memoizedState=null}return t.child}function Nn(e,t,n){if(e!==null&&(t.dependencies=e.dependencies),cl|=t.lanes,(n&t.childLanes)===0)if(e!==null){if(Ya(e,t,n,!1),(n&t.childLanes)===0)return null}else return null;if(e!==null&&t.child!==e.child)throw Error(E(153));if(t.child!==null){for(e=t.child,n=En(e,e.pendingProps),t.child=n,n.return=t;e.sibling!==null;)e=e.sibling,n=n.sibling=En(e,e.pendingProps),n.return=t;n.sibling=null}return t.child}function Ir(e,t){return(e.lanes&t)!==0?!0:(e=e.dependencies,!!(e!==null&&_s(e)))}function Zh(e,t,n){switch(t.tag){case 3:os(t,t.stateNode.containerInfo),Qn(t,Xe,e.memoizedState.cache),zl();break;case 27:case 5:Tc(t);break;case 4:os(t,t.stateNode.containerInfo);break;case 10:Qn(t,t.type,t.memoizedProps.value);break;case 31:if(t.memoizedState!==null)return t.flags|=128,Zc(t),null;break;case 13:var l=t.memoizedState;if(l!==null)return l.dehydrated!==null?(qn(t),t.flags|=128,null):(n&t.child.childLanes)!==0?I0(e,t,n):(qn(t),e=Nn(e,t,n),e!==null?e.sibling:null);qn(t);break;case 19:var a=(e.flags&128)!==0;if(l=(n&t.childLanes)!==0,l||(Ya(e,t,n,!1),l=(n&t.childLanes)!==0),a){if(l)return F0(e,t,n);t.flags|=128}if(a=t.memoizedState,a!==null&&(a.rendering=null,a.tail=null,a.lastEffect=null),ve(Oe,Oe.current),l)break;return null;case 22:return t.lanes=0,W0(e,t,n,t.pendingProps);case 24:Qn(t,Xe,e.memoizedState.cache)}return Nn(e,t,n)}function P0(e,t,n){if(e!==null)if(e.memoizedProps!==t.pendingProps)Qe=!0;else{if(!Ir(e,n)&&(t.flags&128)===0)return Qe=!1,Zh(e,t,n);Qe=(e.flags&131072)!==0}else Qe=!1,ie&&(t.flags&1048576)!==0&&n0(t,Do,t.index);switch(t.lanes=0,t.tag){case 16:e:{var l=t.pendingProps;if(e=Cl(t.elementType),t.type=e,typeof e=="function")Ar(e)?(l=Dl(e,l),t.tag=1,t=Df(null,t,e,l,n)):(t.tag=0,t=Ic(null,t,e,l,n));else{if(e!=null){var a=e.$$typeof;if(a===hr){t.tag=11,t=Af(null,t,e,l,n);break e}else if(a===yr){t.tag=14,t=zf(null,t,e,l,n);break e}}throw t=wc(e)||e,Error(E(306,t,""))}}return t;case 0:return Ic(e,t,t.type,t.pendingProps,n);case 1:return l=t.type,a=Dl(l,t.pendingProps),Df(e,t,l,a,n);case 3:e:{if(os(t,t.stateNode.containerInfo),e===null)throw Error(E(387));l=t.pendingProps;var o=t.memoizedState;a=o.element,Qc(e,t),Co(t,l,null,n);var i=t.memoizedState;if(l=i.cache,Qn(t,Xe,l),l!==o.cache&&jc(t,[Xe],n,!0),xo(),l=i.element,o.isDehydrated)if(o={element:l,isDehydrated:!1,cache:i.cache},t.updateQueue.baseState=o,t.memoizedState=o,t.flags&256){t=Bf(e,t,l,n);break e}else if(l!==a){a=Ht(Error(E(424)),t),Bo(a),t=Bf(e,t,l,n);break e}else for(e=t.stateNode.containerInfo,e.nodeType===9?e=e.body:e=e.nodeName==="HTML"?e.ownerDocument.body:e,Ce=Ut(e.firstChild),Ie=t,ie=!0,Fn=null,Yt=!0,n=u0(t,null,l,n),t.child=n;n;)n.flags=n.flags&-3|4096,n=n.sibling;else{if(zl(),l===a){t=Nn(e,t,n);break e}Je(e,t,l,n)}t=t.child}return t;case 26:return Fi(e,t),e===null?(n=a1(t.type,null,t.pendingProps,null))?t.memoizedState=n:ie||(n=t.type,e=t.pendingProps,l=ks(In.current).createElement(n),l[We]=t,l[mt]=e,Pe(l,n,e),Ve(l),t.stateNode=l):t.memoizedState=a1(t.type,e.memoizedProps,t.pendingProps,e.memoizedState),null;case 27:return Tc(t),e===null&&ie&&(l=t.stateNode=qm(t.type,t.pendingProps,In.current),Ie=t,Yt=!0,a=Ce,dl(t.type)?(_r=a,Ce=Ut(l.firstChild)):Ce=a),Je(e,t,t.pendingProps.children,n),Fi(e,t),e===null&&(t.flags|=4194304),t.child;case 5:return e===null&&ie&&((a=l=Ce)&&(l=by(l,t.type,t.pendingProps,Yt),l!==null?(t.stateNode=l,Ie=t,Ce=Ut(l.firstChild),Yt=!1,a=!0):a=!1),a||sl(t)),Tc(t),a=t.type,o=t.pendingProps,i=e!==null?e.memoizedProps:null,l=o.children,ur(a,o)?l=null:i!==null&&ur(a,i)&&(t.flags|=32),t.memoizedState!==null&&(a=Rr(e,t,Hh,null,null,n),Xo._currentValue=a),Fi(e,t),Je(e,t,l,n),t.child;case 6:return e===null&&ie&&((e=n=Ce)&&(n=vy(n,t.pendingProps,Yt),n!==null?(t.stateNode=n,Ie=t,Ce=null,e=!0):e=!1),e||sl(t)),null;case 13:return I0(e,t,n);case 4:return os(t,t.stateNode.containerInfo),l=t.pendingProps,e===null?t.child=Ll(t,null,l,n):Je(e,t,l,n),t.child;case 11:return Af(e,t,t.type,t.pendingProps,n);case 7:return Je(e,t,t.pendingProps,n),t.child;case 8:return Je(e,t,t.pendingProps.children,n),t.child;case 12:return Je(e,t,t.pendingProps.children,n),t.child;case 10:return l=t.pendingProps,Qn(t,t.type,l.value),Je(e,t,l.children,n),t.child;case 9:return a=t.type._context,l=t.pendingProps.children,Nl(t),a=Fe(a),l=l(a),t.flags|=1,Je(e,t,l,n),t.child;case 14:return zf(e,t,t.type,t.pendingProps,n);case 15:return J0(e,t,t.type,t.pendingProps,n);case 19:return F0(e,t,n);case 31:return $h(e,t,n);case 22:return W0(e,t,n,t.pendingProps);case 24:return Nl(t),l=Fe(Xe),e===null?(a=Or(),a===null&&(a=ge,o=Lr(),a.pooledCache=o,o.refCount++,o!==null&&(a.pooledCacheLanes|=n),a=o),t.memoizedState={parent:l,cache:a},Br(t),Qn(t,Xe,a)):((e.lanes&n)!==0&&(Qc(e,t),Co(t,null,null,n),xo()),a=e.memoizedState,o=t.memoizedState,a.parent!==l?(a={parent:l,cache:l},t.memoizedState=a,t.lanes===0&&(t.memoizedState=t.updateQueue.baseState=a),Qn(t,Xe,l)):(l=o.cache,Qn(t,Xe,l),l!==a.cache&&jc(t,[Xe],n,!0))),Je(e,t,t.pendingProps.children,n),t.child;case 29:throw t.pendingProps}throw Error(E(156,t.tag))}function yn(e){e.flags|=4}function cc(e,t,n,l,a){if((t=(e.mode&32)!==0)&&(t=!1),t){if(e.flags|=16777216,(a&335544128)===a)if(e.stateNode.complete)e.flags|=8192;else if(Cm())e.flags|=8192;else throw Ml=fs,Dr}else e.flags&=-16777217}function Yf(e,t){if(t.type!=="stylesheet"||(t.state.loading&4)!==0)e.flags&=-16777217;else if(e.flags|=16777216,!Gm(t))if(Cm())e.flags|=8192;else throw Ml=fs,Dr}function Hi(e,t){t!==null&&(e.flags|=4),e.flags&16384&&(t=e.tag!==22?w1():536870912,e.lanes|=t,za|=t)}function so(e,t){if(!ie)switch(e.tailMode){case"hidden":t=e.tail;for(var n=null;t!==null;)t.alternate!==null&&(n=t),t=t.sibling;n===null?e.tail=null:n.sibling=null;break;case"collapsed":n=e.tail;for(var l=null;n!==null;)n.alternate!==null&&(l=n),n=n.sibling;l===null?t||e.tail===null?e.tail=null:e.tail.sibling=null:l.sibling=null}}function xe(e){var t=e.alternate!==null&&e.alternate.child===e.child,n=0,l=0;if(t)for(var a=e.child;a!==null;)n|=a.lanes|a.childLanes,l|=a.subtreeFlags&65011712,l|=a.flags&65011712,a.return=e,a=a.sibling;else for(a=e.child;a!==null;)n|=a.lanes|a.childLanes,l|=a.subtreeFlags,l|=a.flags,a.return=e,a=a.sibling;return e.subtreeFlags|=l,e.childLanes=n,t}function Gh(e,t,n){var l=t.pendingProps;switch(Nr(t),t.tag){case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return xe(t),null;case 1:return xe(t),null;case 3:return n=t.stateNode,l=null,e!==null&&(l=e.memoizedState.cache),t.memoizedState.cache!==l&&(t.flags|=2048),Tn(Xe),wa(),n.pendingContext&&(n.context=n.pendingContext,n.pendingContext=null),(e===null||e.child===null)&&(ta(t)?yn(t):e===null||e.memoizedState.isDehydrated&&(t.flags&256)===0||(t.flags|=1024,ec())),xe(t),null;case 26:var a=t.type,o=t.memoizedState;return e===null?(yn(t),o!==null?(xe(t),Yf(t,o)):(xe(t),cc(t,a,null,l,n))):o?o!==e.memoizedState?(yn(t),xe(t),Yf(t,o)):(xe(t),t.flags&=-16777217):(e=e.memoizedProps,e!==l&&yn(t),xe(t),cc(t,a,e,l,n)),null;case 27:if(is(t),n=In.current,a=t.type,e!==null&&t.stateNode!=null)e.memoizedProps!==l&&yn(t);else{if(!l){if(t.stateNode===null)throw Error(E(166));return xe(t),null}e=tn.current,ta(t)?_f(t,e):(e=qm(a,l,n),t.stateNode=e,yn(t))}return xe(t),null;case 5:if(is(t),a=t.type,e!==null&&t.stateNode!=null)e.memoizedProps!==l&&yn(t);else{if(!l){if(t.stateNode===null)throw Error(E(166));return xe(t),null}if(o=tn.current,ta(t))_f(t,o);else{var i=ks(In.current);switch(o){case 1:o=i.createElementNS("http://www.w3.org/2000/svg",a);break;case 2:o=i.createElementNS("http://www.w3.org/1998/Math/MathML",a);break;default:switch(a){case"svg":o=i.createElementNS("http://www.w3.org/2000/svg",a);break;case"math":o=i.createElementNS("http://www.w3.org/1998/Math/MathML",a);break;case"script":o=i.createElement("div"),o.innerHTML="<script><\/script>",o=o.removeChild(o.firstChild);break;case"select":o=typeof l.is=="string"?i.createElement("select",{is:l.is}):i.createElement("select"),l.multiple?o.multiple=!0:l.size&&(o.size=l.size);break;default:o=typeof l.is=="string"?i.createElement(a,{is:l.is}):i.createElement(a)}}o[We]=t,o[mt]=l;e:for(i=t.child;i!==null;){if(i.tag===5||i.tag===6)o.appendChild(i.stateNode);else if(i.tag!==4&&i.tag!==27&&i.child!==null){i.child.return=i,i=i.child;continue}if(i===t)break e;for(;i.sibling===null;){if(i.return===null||i.return===t)break e;i=i.return}i.sibling.return=i.return,i=i.sibling}t.stateNode=o;e:switch(Pe(o,a,l),a){case"button":case"input":case"select":case"textarea":l=!!l.autoFocus;break e;case"img":l=!0;break e;default:l=!1}l&&yn(t)}}return xe(t),cc(t,t.type,e===null?null:e.memoizedProps,t.pendingProps,n),null;case 6:if(e&&t.stateNode!=null)e.memoizedProps!==l&&yn(t);else{if(typeof l!="string"&&t.stateNode===null)throw Error(E(166));if(e=In.current,ta(t)){if(e=t.stateNode,n=t.memoizedProps,l=null,a=Ie,a!==null)switch(a.tag){case 27:case 5:l=a.memoizedProps}e[We]=t,e=!!(e.nodeValue===n||l!==null&&l.suppressHydrationWarning===!0||Um(e.nodeValue,n)),e||sl(t,!0)}else e=ks(e).createTextNode(l),e[We]=t,t.stateNode=e}return xe(t),null;case 31:if(n=t.memoizedState,e===null||e.memoizedState!==null){if(l=ta(t),n!==null){if(e===null){if(!l)throw Error(E(318));if(e=t.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(E(557));e[We]=t}else zl(),(t.flags&128)===0&&(t.memoizedState=null),t.flags|=4;xe(t),e=!1}else n=ec(),e!==null&&e.memoizedState!==null&&(e.memoizedState.hydrationErrors=n),e=!0;if(!e)return t.flags&256?(St(t),t):(St(t),null);if((t.flags&128)!==0)throw Error(E(558))}return xe(t),null;case 13:if(l=t.memoizedState,e===null||e.memoizedState!==null&&e.memoizedState.dehydrated!==null){if(a=ta(t),l!==null&&l.dehydrated!==null){if(e===null){if(!a)throw Error(E(318));if(a=t.memoizedState,a=a!==null?a.dehydrated:null,!a)throw Error(E(317));a[We]=t}else zl(),(t.flags&128)===0&&(t.memoizedState=null),t.flags|=4;xe(t),a=!1}else a=ec(),e!==null&&e.memoizedState!==null&&(e.memoizedState.hydrationErrors=a),a=!0;if(!a)return t.flags&256?(St(t),t):(St(t),null)}return St(t),(t.flags&128)!==0?(t.lanes=n,t):(n=l!==null,e=e!==null&&e.memoizedState!==null,n&&(l=t.child,a=null,l.alternate!==null&&l.alternate.memoizedState!==null&&l.alternate.memoizedState.cachePool!==null&&(a=l.alternate.memoizedState.cachePool.pool),o=null,l.memoizedState!==null&&l.memoizedState.cachePool!==null&&(o=l.memoizedState.cachePool.pool),o!==a&&(l.flags|=2048)),n!==e&&n&&(t.child.flags|=8192),Hi(t,t.updateQueue),xe(t),null);case 4:return wa(),e===null&&ad(t.stateNode.containerInfo),xe(t),null;case 10:return Tn(t.type),xe(t),null;case 19:if(Ke(Oe),l=t.memoizedState,l===null)return xe(t),null;if(a=(t.flags&128)!==0,o=l.rendering,o===null)if(a)so(l,!1);else{if(Ne!==0||e!==null&&(e.flags&128)!==0)for(e=t.child;e!==null;){if(o=hs(e),o!==null){for(t.flags|=128,so(l,!1),e=o.updateQueue,t.updateQueue=e,Hi(t,e),t.subtreeFlags=0,e=n,n=t.child;n!==null;)e0(n,e),n=n.sibling;return ve(Oe,Oe.current&1|2),ie&&vn(t,l.treeForkCount),t.child}e=e.sibling}l.tail!==null&&wt()>Ss&&(t.flags|=128,a=!0,so(l,!1),t.lanes=4194304)}else{if(!a)if(e=hs(o),e!==null){if(t.flags|=128,a=!0,e=e.updateQueue,t.updateQueue=e,Hi(t,e),so(l,!0),l.tail===null&&l.tailMode==="hidden"&&!o.alternate&&!ie)return xe(t),null}else 2*wt()-l.renderingStartTime>Ss&&n!==536870912&&(t.flags|=128,a=!0,so(l,!1),t.lanes=4194304);l.isBackwards?(o.sibling=t.child,t.child=o):(e=l.last,e!==null?e.sibling=o:t.child=o,l.last=o)}return l.tail!==null?(e=l.tail,l.rendering=e,l.tail=e.sibling,l.renderingStartTime=wt(),e.sibling=null,n=Oe.current,ve(Oe,a?n&1|2:n&1),ie&&vn(t,l.treeForkCount),e):(xe(t),null);case 22:case 23:return St(t),Hr(),l=t.memoizedState!==null,e!==null?e.memoizedState!==null!==l&&(t.flags|=8192):l&&(t.flags|=8192),l?(n&536870912)!==0&&(t.flags&128)===0&&(xe(t),t.subtreeFlags&6&&(t.flags|=8192)):xe(t),n=t.updateQueue,n!==null&&Hi(t,n.retryQueue),n=null,e!==null&&e.memoizedState!==null&&e.memoizedState.cachePool!==null&&(n=e.memoizedState.cachePool.pool),l=null,t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(l=t.memoizedState.cachePool.pool),l!==n&&(t.flags|=2048),e!==null&&Ke(kl),null;case 24:return n=null,e!==null&&(n=e.memoizedState.cache),t.memoizedState.cache!==n&&(t.flags|=2048),Tn(Xe),xe(t),null;case 25:return null;case 30:return null}throw Error(E(156,t.tag))}function Vh(e,t){switch(Nr(t),t.tag){case 1:return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 3:return Tn(Xe),wa(),e=t.flags,(e&65536)!==0&&(e&128)===0?(t.flags=e&-65537|128,t):null;case 26:case 27:case 5:return is(t),null;case 31:if(t.memoizedState!==null){if(St(t),t.alternate===null)throw Error(E(340));zl()}return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 13:if(St(t),e=t.memoizedState,e!==null&&e.dehydrated!==null){if(t.alternate===null)throw Error(E(340));zl()}return e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 19:return Ke(Oe),null;case 4:return wa(),null;case 10:return Tn(t.type),null;case 22:case 23:return St(t),Hr(),e!==null&&Ke(kl),e=t.flags,e&65536?(t.flags=e&-65537|128,t):null;case 24:return Tn(Xe),null;case 25:return null;default:return null}}function em(e,t){switch(Nr(t),t.tag){case 3:Tn(Xe),wa();break;case 26:case 27:case 5:is(t);break;case 4:wa();break;case 31:t.memoizedState!==null&&St(t);break;case 13:St(t);break;case 19:Ke(Oe);break;case 10:Tn(t.type);break;case 22:case 23:St(t),Hr(),e!==null&&Ke(kl);break;case 24:Tn(Xe)}}function Fo(e,t){try{var n=t.updateQueue,l=n!==null?n.lastEffect:null;if(l!==null){var a=l.next;n=a;do{if((n.tag&e)===e){l=void 0;var o=n.create,i=n.inst;l=o(),i.destroy=l}n=n.next}while(n!==a)}}catch(s){_e(t,t.return,s)}}function ul(e,t,n){try{var l=t.updateQueue,a=l!==null?l.lastEffect:null;if(a!==null){var o=a.next;l=o;do{if((l.tag&e)===e){var i=l.inst,s=i.destroy;if(s!==void 0){i.destroy=void 0,a=t;var u=n,h=s;try{h()}catch(y){_e(a,u,y)}}}l=l.next}while(l!==o)}}catch(y){_e(t,t.return,y)}}function tm(e){var t=e.updateQueue;if(t!==null){var n=e.stateNode;try{r0(t,n)}catch(l){_e(e,e.return,l)}}}function nm(e,t,n){n.props=Dl(e.type,e.memoizedProps),n.state=e.memoizedState;try{n.componentWillUnmount()}catch(l){_e(e,t,l)}}function Eo(e,t){try{var n=e.ref;if(n!==null){switch(e.tag){case 26:case 27:case 5:var l=e.stateNode;break;case 30:l=e.stateNode;break;default:l=e.stateNode}typeof n=="function"?e.refCleanup=n(l):n.current=l}}catch(a){_e(e,t,a)}}function en(e,t){var n=e.ref,l=e.refCleanup;if(n!==null)if(typeof l=="function")try{l()}catch(a){_e(e,t,a)}finally{e.refCleanup=null,e=e.alternate,e!=null&&(e.refCleanup=null)}else if(typeof n=="function")try{n(null)}catch(a){_e(e,t,a)}else n.current=null}function lm(e){var t=e.type,n=e.memoizedProps,l=e.stateNode;try{e:switch(t){case"button":case"input":case"select":case"textarea":n.autoFocus&&l.focus();break e;case"img":n.src?l.src=n.src:n.srcSet&&(l.srcset=n.srcSet)}}catch(a){_e(e,e.return,a)}}function rc(e,t,n){try{var l=e.stateNode;fy(l,e.type,n,t),l[mt]=t}catch(a){_e(e,e.return,a)}}function am(e){return e.tag===5||e.tag===3||e.tag===26||e.tag===27&&dl(e.type)||e.tag===4}function dc(e){e:for(;;){for(;e.sibling===null;){if(e.return===null||am(e.return))return null;e=e.return}for(e.sibling.return=e.return,e=e.sibling;e.tag!==5&&e.tag!==6&&e.tag!==18;){if(e.tag===27&&dl(e.type)||e.flags&2||e.child===null||e.tag===4)continue e;e.child.return=e,e=e.child}if(!(e.flags&2))return e.stateNode}}function Pc(e,t,n){var l=e.tag;if(l===5||l===6)e=e.stateNode,t?(n.nodeType===9?n.body:n.nodeName==="HTML"?n.ownerDocument.body:n).insertBefore(e,t):(t=n.nodeType===9?n.body:n.nodeName==="HTML"?n.ownerDocument.body:n,t.appendChild(e),n=n._reactRootContainer,n!=null||t.onclick!==null||(t.onclick=Cn));else if(l!==4&&(l===27&&dl(e.type)&&(n=e.stateNode,t=null),e=e.child,e!==null))for(Pc(e,t,n),e=e.sibling;e!==null;)Pc(e,t,n),e=e.sibling}function vs(e,t,n){var l=e.tag;if(l===5||l===6)e=e.stateNode,t?n.insertBefore(e,t):n.appendChild(e);else if(l!==4&&(l===27&&dl(e.type)&&(n=e.stateNode),e=e.child,e!==null))for(vs(e,t,n),e=e.sibling;e!==null;)vs(e,t,n),e=e.sibling}function om(e){var t=e.stateNode,n=e.memoizedProps;try{for(var l=e.type,a=t.attributes;a.length;)t.removeAttributeNode(a[0]);Pe(t,l,n),t[We]=e,t[mt]=n}catch(o){_e(e,e.return,o)}}var Sn=!1,je=!1,_c=!1,Rf=typeof WeakSet=="function"?WeakSet:Set,Ge=null;function Kh(e,t){if(e=e.containerInfo,ir=Ns,e=G1(e),Tr(e)){if("selectionStart"in e)var n={start:e.selectionStart,end:e.selectionEnd};else e:{n=(n=e.ownerDocument)&&n.defaultView||window;var l=n.getSelection&&n.getSelection();if(l&&l.rangeCount!==0){n=l.anchorNode;var a=l.anchorOffset,o=l.focusNode;l=l.focusOffset;try{n.nodeType,o.nodeType}catch{n=null;break e}var i=0,s=-1,u=-1,h=0,y=0,S=e,p=null;t:for(;;){for(var b;S!==n||a!==0&&S.nodeType!==3||(s=i+a),S!==o||l!==0&&S.nodeType!==3||(u=i+l),S.nodeType===3&&(i+=S.nodeValue.length),(b=S.firstChild)!==null;)p=S,S=b;for(;;){if(S===e)break t;if(p===n&&++h===a&&(s=i),p===o&&++y===l&&(u=i),(b=S.nextSibling)!==null)break;S=p,p=S.parentNode}S=b}n=s===-1||u===-1?null:{start:s,end:u}}else n=null}n=n||{start:0,end:0}}else n=null;for(sr={focusedElem:e,selectionRange:n},Ns=!1,Ge=t;Ge!==null;)if(t=Ge,e=t.child,(t.subtreeFlags&1028)!==0&&e!==null)e.return=t,Ge=e;else for(;Ge!==null;){switch(t=Ge,o=t.alternate,e=t.flags,t.tag){case 0:if((e&4)!==0&&(e=t.updateQueue,e=e!==null?e.events:null,e!==null))for(n=0;n<e.length;n++)a=e[n],a.ref.impl=a.nextImpl;break;case 11:case 15:break;case 1:if((e&1024)!==0&&o!==null){e=void 0,n=t,a=o.memoizedProps,o=o.memoizedState,l=n.stateNode;try{var A=Dl(n.type,a);e=l.getSnapshotBeforeUpdate(A,o),l.__reactInternalSnapshotBeforeUpdate=e}catch(k){_e(n,n.return,k)}}break;case 3:if((e&1024)!==0){if(e=t.stateNode.containerInfo,n=e.nodeType,n===9)cr(e);else if(n===1)switch(e.nodeName){case"HEAD":case"HTML":case"BODY":cr(e);break;default:e.textContent=""}}break;case 5:case 26:case 27:case 6:case 4:case 17:break;default:if((e&1024)!==0)throw Error(E(163))}if(e=t.sibling,e!==null){e.return=t.return,Ge=e;break}Ge=t.return}}function im(e,t,n){var l=n.flags;switch(n.tag){case 0:case 11:case 15:pn(e,n),l&4&&Fo(5,n);break;case 1:if(pn(e,n),l&4)if(e=n.stateNode,t===null)try{e.componentDidMount()}catch(i){_e(n,n.return,i)}else{var a=Dl(n.type,t.memoizedProps);t=t.memoizedState;try{e.componentDidUpdate(a,t,e.__reactInternalSnapshotBeforeUpdate)}catch(i){_e(n,n.return,i)}}l&64&&tm(n),l&512&&Eo(n,n.return);break;case 3:if(pn(e,n),l&64&&(e=n.updateQueue,e!==null)){if(t=null,n.child!==null)switch(n.child.tag){case 27:case 5:t=n.child.stateNode;break;case 1:t=n.child.stateNode}try{r0(e,t)}catch(i){_e(n,n.return,i)}}break;case 27:t===null&&l&4&&om(n);case 26:case 5:pn(e,n),t===null&&l&4&&lm(n),l&512&&Eo(n,n.return);break;case 12:pn(e,n);break;case 31:pn(e,n),l&4&&cm(e,n);break;case 13:pn(e,n),l&4&&rm(e,n),l&64&&(e=n.memoizedState,e!==null&&(e=e.dehydrated,e!==null&&(n=ly.bind(null,n),Sy(e,n))));break;case 22:if(l=n.memoizedState!==null||Sn,!l){t=t!==null&&t.memoizedState!==null||je,a=Sn;var o=je;Sn=l,(je=t)&&!o?bn(e,n,(n.subtreeFlags&8772)!==0):pn(e,n),Sn=a,je=o}break;case 30:break;default:pn(e,n)}}function sm(e){var t=e.alternate;t!==null&&(e.alternate=null,sm(t)),e.child=null,e.deletions=null,e.sibling=null,e.tag===5&&(t=e.stateNode,t!==null&&vr(t)),e.stateNode=null,e.return=null,e.dependencies=null,e.memoizedProps=null,e.memoizedState=null,e.pendingProps=null,e.stateNode=null,e.updateQueue=null}var Te=null,dt=!1;function gn(e,t,n){for(n=n.child;n!==null;)um(e,t,n),n=n.sibling}function um(e,t,n){if(Et&&typeof Et.onCommitFiberUnmount=="function")try{Et.onCommitFiberUnmount(Zo,n)}catch{}switch(n.tag){case 26:je||en(n,t),gn(e,t,n),n.memoizedState?n.memoizedState.count--:n.stateNode&&(n=n.stateNode,n.parentNode.removeChild(n));break;case 27:je||en(n,t);var l=Te,a=dt;dl(n.type)&&(Te=n.stateNode,dt=!1),gn(e,t,n),Ao(n.stateNode),Te=l,dt=a;break;case 5:je||en(n,t);case 6:if(l=Te,a=dt,Te=null,gn(e,t,n),Te=l,dt=a,Te!==null)if(dt)try{(Te.nodeType===9?Te.body:Te.nodeName==="HTML"?Te.ownerDocument.body:Te).removeChild(n.stateNode)}catch(o){_e(n,t,o)}else try{Te.removeChild(n.stateNode)}catch(o){_e(n,t,o)}break;case 18:Te!==null&&(dt?(e=Te,Pf(e.nodeType===9?e.body:e.nodeName==="HTML"?e.ownerDocument.body:e,n.stateNode),Da(e)):Pf(Te,n.stateNode));break;case 4:l=Te,a=dt,Te=n.stateNode.containerInfo,dt=!0,gn(e,t,n),Te=l,dt=a;break;case 0:case 11:case 14:case 15:ul(2,n,t),je||ul(4,n,t),gn(e,t,n);break;case 1:je||(en(n,t),l=n.stateNode,typeof l.componentWillUnmount=="function"&&nm(n,t,l)),gn(e,t,n);break;case 21:gn(e,t,n);break;case 22:je=(l=je)||n.memoizedState!==null,gn(e,t,n),je=l;break;default:gn(e,t,n)}}function cm(e,t){if(t.memoizedState===null&&(e=t.alternate,e!==null&&(e=e.memoizedState,e!==null))){e=e.dehydrated;try{Da(e)}catch(n){_e(t,t.return,n)}}}function rm(e,t){if(t.memoizedState===null&&(e=t.alternate,e!==null&&(e=e.memoizedState,e!==null&&(e=e.dehydrated,e!==null))))try{Da(e)}catch(n){_e(t,t.return,n)}}function Jh(e){switch(e.tag){case 31:case 13:case 19:var t=e.stateNode;return t===null&&(t=e.stateNode=new Rf),t;case 22:return e=e.stateNode,t=e._retryCache,t===null&&(t=e._retryCache=new Rf),t;default:throw Error(E(435,e.tag))}}function Yi(e,t){var n=Jh(e);t.forEach(function(l){if(!n.has(l)){n.add(l);var a=ay.bind(null,e,l);l.then(a,a)}})}function ct(e,t){var n=t.deletions;if(n!==null)for(var l=0;l<n.length;l++){var a=n[l],o=e,i=t,s=i;e:for(;s!==null;){switch(s.tag){case 27:if(dl(s.type)){Te=s.stateNode,dt=!1;break e}break;case 5:Te=s.stateNode,dt=!1;break e;case 3:case 4:Te=s.stateNode.containerInfo,dt=!0;break e}s=s.return}if(Te===null)throw Error(E(160));um(o,i,a),Te=null,dt=!1,o=a.alternate,o!==null&&(o.return=null),a.return=null}if(t.subtreeFlags&13886)for(t=t.child;t!==null;)dm(t,e),t=t.sibling}var $t=null;function dm(e,t){var n=e.alternate,l=e.flags;switch(e.tag){case 0:case 11:case 14:case 15:ct(t,e),rt(e),l&4&&(ul(3,e,e.return),Fo(3,e),ul(5,e,e.return));break;case 1:ct(t,e),rt(e),l&512&&(je||n===null||en(n,n.return)),l&64&&Sn&&(e=e.updateQueue,e!==null&&(l=e.callbacks,l!==null&&(n=e.shared.hiddenCallbacks,e.shared.hiddenCallbacks=n===null?l:n.concat(l))));break;case 26:var a=$t;if(ct(t,e),rt(e),l&512&&(je||n===null||en(n,n.return)),l&4){var o=n!==null?n.memoizedState:null;if(l=e.memoizedState,n===null)if(l===null)if(e.stateNode===null){e:{l=e.type,n=e.memoizedProps,a=a.ownerDocument||a;t:switch(l){case"title":o=a.getElementsByTagName("title")[0],(!o||o[Ko]||o[We]||o.namespaceURI==="http://www.w3.org/2000/svg"||o.hasAttribute("itemprop"))&&(o=a.createElement(l),a.head.insertBefore(o,a.querySelector("head > title"))),Pe(o,l,n),o[We]=e,Ve(o),l=o;break e;case"link":var i=i1("link","href",a).get(l+(n.href||""));if(i){for(var s=0;s<i.length;s++)if(o=i[s],o.getAttribute("href")===(n.href==null||n.href===""?null:n.href)&&o.getAttribute("rel")===(n.rel==null?null:n.rel)&&o.getAttribute("title")===(n.title==null?null:n.title)&&o.getAttribute("crossorigin")===(n.crossOrigin==null?null:n.crossOrigin)){i.splice(s,1);break t}}o=a.createElement(l),Pe(o,l,n),a.head.appendChild(o);break;case"meta":if(i=i1("meta","content",a).get(l+(n.content||""))){for(s=0;s<i.length;s++)if(o=i[s],o.getAttribute("content")===(n.content==null?null:""+n.content)&&o.getAttribute("name")===(n.name==null?null:n.name)&&o.getAttribute("property")===(n.property==null?null:n.property)&&o.getAttribute("http-equiv")===(n.httpEquiv==null?null:n.httpEquiv)&&o.getAttribute("charset")===(n.charSet==null?null:n.charSet)){i.splice(s,1);break t}}o=a.createElement(l),Pe(o,l,n),a.head.appendChild(o);break;default:throw Error(E(468,l))}o[We]=e,Ve(o),l=o}e.stateNode=l}else s1(a,e.type,e.stateNode);else e.stateNode=o1(a,l,e.memoizedProps);else o!==l?(o===null?n.stateNode!==null&&(n=n.stateNode,n.parentNode.removeChild(n)):o.count--,l===null?s1(a,e.type,e.stateNode):o1(a,l,e.memoizedProps)):l===null&&e.stateNode!==null&&rc(e,e.memoizedProps,n.memoizedProps)}break;case 27:ct(t,e),rt(e),l&512&&(je||n===null||en(n,n.return)),n!==null&&l&4&&rc(e,e.memoizedProps,n.memoizedProps);break;case 5:if(ct(t,e),rt(e),l&512&&(je||n===null||en(n,n.return)),e.flags&32){a=e.stateNode;try{Ta(a,"")}catch(A){_e(e,e.return,A)}}l&4&&e.stateNode!=null&&(a=e.memoizedProps,rc(e,a,n!==null?n.memoizedProps:a)),l&1024&&(_c=!0);break;case 6:if(ct(t,e),rt(e),l&4){if(e.stateNode===null)throw Error(E(162));l=e.memoizedProps,n=e.stateNode;try{n.nodeValue=l}catch(A){_e(e,e.return,A)}}break;case 3:if(ts=null,a=$t,$t=Ms(t.containerInfo),ct(t,e),$t=a,rt(e),l&4&&n!==null&&n.memoizedState.isDehydrated)try{Da(t.containerInfo)}catch(A){_e(e,e.return,A)}_c&&(_c=!1,_m(e));break;case 4:l=$t,$t=Ms(e.stateNode.containerInfo),ct(t,e),rt(e),$t=l;break;case 12:ct(t,e),rt(e);break;case 31:ct(t,e),rt(e),l&4&&(l=e.updateQueue,l!==null&&(e.updateQueue=null,Yi(e,l)));break;case 13:ct(t,e),rt(e),e.child.flags&8192&&e.memoizedState!==null!=(n!==null&&n.memoizedState!==null)&&($s=wt()),l&4&&(l=e.updateQueue,l!==null&&(e.updateQueue=null,Yi(e,l)));break;case 22:a=e.memoizedState!==null;var u=n!==null&&n.memoizedState!==null,h=Sn,y=je;if(Sn=h||a,je=y||u,ct(t,e),je=y,Sn=h,rt(e),l&8192)e:for(t=e.stateNode,t._visibility=a?t._visibility&-2:t._visibility|1,a&&(n===null||u||Sn||je||wl(e)),n=null,t=e;;){if(t.tag===5||t.tag===26){if(n===null){u=n=t;try{if(o=u.stateNode,a)i=o.style,typeof i.setProperty=="function"?i.setProperty("display","none","important"):i.display="none";else{s=u.stateNode;var S=u.memoizedProps.style,p=S!=null&&S.hasOwnProperty("display")?S.display:null;s.style.display=p==null||typeof p=="boolean"?"":(""+p).trim()}}catch(A){_e(u,u.return,A)}}}else if(t.tag===6){if(n===null){u=t;try{u.stateNode.nodeValue=a?"":u.memoizedProps}catch(A){_e(u,u.return,A)}}}else if(t.tag===18){if(n===null){u=t;try{var b=u.stateNode;a?e1(b,!0):e1(u.stateNode,!1)}catch(A){_e(u,u.return,A)}}}else if((t.tag!==22&&t.tag!==23||t.memoizedState===null||t===e)&&t.child!==null){t.child.return=t,t=t.child;continue}if(t===e)break e;for(;t.sibling===null;){if(t.return===null||t.return===e)break e;n===t&&(n=null),t=t.return}n===t&&(n=null),t.sibling.return=t.return,t=t.sibling}l&4&&(l=e.updateQueue,l!==null&&(n=l.retryQueue,n!==null&&(l.retryQueue=null,Yi(e,n))));break;case 19:ct(t,e),rt(e),l&4&&(l=e.updateQueue,l!==null&&(e.updateQueue=null,Yi(e,l)));break;case 30:break;case 21:break;default:ct(t,e),rt(e)}}function rt(e){var t=e.flags;if(t&2){try{for(var n,l=e.return;l!==null;){if(am(l)){n=l;break}l=l.return}if(n==null)throw Error(E(160));switch(n.tag){case 27:var a=n.stateNode,o=dc(e);vs(e,o,a);break;case 5:var i=n.stateNode;n.flags&32&&(Ta(i,""),n.flags&=-33);var s=dc(e);vs(e,s,i);break;case 3:case 4:var u=n.stateNode.containerInfo,h=dc(e);Pc(e,h,u);break;default:throw Error(E(161))}}catch(y){_e(e,e.return,y)}e.flags&=-3}t&4096&&(e.flags&=-4097)}function _m(e){if(e.subtreeFlags&1024)for(e=e.child;e!==null;){var t=e;_m(t),t.tag===5&&t.flags&1024&&t.stateNode.reset(),e=e.sibling}}function pn(e,t){if(t.subtreeFlags&8772)for(t=t.child;t!==null;)im(e,t.alternate,t),t=t.sibling}function wl(e){for(e=e.child;e!==null;){var t=e;switch(t.tag){case 0:case 11:case 14:case 15:ul(4,t,t.return),wl(t);break;case 1:en(t,t.return);var n=t.stateNode;typeof n.componentWillUnmount=="function"&&nm(t,t.return,n),wl(t);break;case 27:Ao(t.stateNode);case 26:case 5:en(t,t.return),wl(t);break;case 22:t.memoizedState===null&&wl(t);break;case 30:wl(t);break;default:wl(t)}e=e.sibling}}function bn(e,t,n){for(n=n&&(t.subtreeFlags&8772)!==0,t=t.child;t!==null;){var l=t.alternate,a=e,o=t,i=o.flags;switch(o.tag){case 0:case 11:case 15:bn(a,o,n),Fo(4,o);break;case 1:if(bn(a,o,n),l=o,a=l.stateNode,typeof a.componentDidMount=="function")try{a.componentDidMount()}catch(h){_e(l,l.return,h)}if(l=o,a=l.updateQueue,a!==null){var s=l.stateNode;try{var u=a.shared.hiddenCallbacks;if(u!==null)for(a.shared.hiddenCallbacks=null,a=0;a<u.length;a++)c0(u[a],s)}catch(h){_e(l,l.return,h)}}n&&i&64&&tm(o),Eo(o,o.return);break;case 27:om(o);case 26:case 5:bn(a,o,n),n&&l===null&&i&4&&lm(o),Eo(o,o.return);break;case 12:bn(a,o,n);break;case 31:bn(a,o,n),n&&i&4&&cm(a,o);break;case 13:bn(a,o,n),n&&i&4&&rm(a,o);break;case 22:o.memoizedState===null&&bn(a,o,n),Eo(o,o.return);break;case 30:break;default:bn(a,o,n)}t=t.sibling}}function Fr(e,t){var n=null;e!==null&&e.memoizedState!==null&&e.memoizedState.cachePool!==null&&(n=e.memoizedState.cachePool.pool),e=null,t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(e=t.memoizedState.cachePool.pool),e!==n&&(e!=null&&e.refCount++,n!=null&&Wo(n))}function Pr(e,t){e=null,t.alternate!==null&&(e=t.alternate.memoizedState.cache),t=t.memoizedState.cache,t!==e&&(t.refCount++,e!=null&&Wo(e))}function qt(e,t,n,l){if(t.subtreeFlags&10256)for(t=t.child;t!==null;)fm(e,t,n,l),t=t.sibling}function fm(e,t,n,l){var a=t.flags;switch(t.tag){case 0:case 11:case 15:qt(e,t,n,l),a&2048&&Fo(9,t);break;case 1:qt(e,t,n,l);break;case 3:qt(e,t,n,l),a&2048&&(e=null,t.alternate!==null&&(e=t.alternate.memoizedState.cache),t=t.memoizedState.cache,t!==e&&(t.refCount++,e!=null&&Wo(e)));break;case 12:if(a&2048){qt(e,t,n,l),e=t.stateNode;try{var o=t.memoizedProps,i=o.id,s=o.onPostCommit;typeof s=="function"&&s(i,t.alternate===null?"mount":"update",e.passiveEffectDuration,-0)}catch(u){_e(t,t.return,u)}}else qt(e,t,n,l);break;case 31:qt(e,t,n,l);break;case 13:qt(e,t,n,l);break;case 23:break;case 22:o=t.stateNode,i=t.alternate,t.memoizedState!==null?o._visibility&2?qt(e,t,n,l):To(e,t):o._visibility&2?qt(e,t,n,l):(o._visibility|=2,la(e,t,n,l,(t.subtreeFlags&10256)!==0||!1)),a&2048&&Fr(i,t);break;case 24:qt(e,t,n,l),a&2048&&Pr(t.alternate,t);break;default:qt(e,t,n,l)}}function la(e,t,n,l,a){for(a=a&&((t.subtreeFlags&10256)!==0||!1),t=t.child;t!==null;){var o=e,i=t,s=n,u=l,h=i.flags;switch(i.tag){case 0:case 11:case 15:la(o,i,s,u,a),Fo(8,i);break;case 23:break;case 22:var y=i.stateNode;i.memoizedState!==null?y._visibility&2?la(o,i,s,u,a):To(o,i):(y._visibility|=2,la(o,i,s,u,a)),a&&h&2048&&Fr(i.alternate,i);break;case 24:la(o,i,s,u,a),a&&h&2048&&Pr(i.alternate,i);break;default:la(o,i,s,u,a)}t=t.sibling}}function To(e,t){if(t.subtreeFlags&10256)for(t=t.child;t!==null;){var n=e,l=t,a=l.flags;switch(l.tag){case 22:To(n,l),a&2048&&Fr(l.alternate,l);break;case 24:To(n,l),a&2048&&Pr(l.alternate,l);break;default:To(n,l)}t=t.sibling}}var yo=8192;function na(e,t,n){if(e.subtreeFlags&yo)for(e=e.child;e!==null;)mm(e,t,n),e=e.sibling}function mm(e,t,n){switch(e.tag){case 26:na(e,t,n),e.flags&yo&&e.memoizedState!==null&&Oy(n,$t,e.memoizedState,e.memoizedProps);break;case 5:na(e,t,n);break;case 3:case 4:var l=$t;$t=Ms(e.stateNode.containerInfo),na(e,t,n),$t=l;break;case 22:e.memoizedState===null&&(l=e.alternate,l!==null&&l.memoizedState!==null?(l=yo,yo=16777216,na(e,t,n),yo=l):na(e,t,n));break;default:na(e,t,n)}}function hm(e){var t=e.alternate;if(t!==null&&(e=t.child,e!==null)){t.child=null;do t=e.sibling,e.sibling=null,e=t;while(e!==null)}}function uo(e){var t=e.deletions;if((e.flags&16)!==0){if(t!==null)for(var n=0;n<t.length;n++){var l=t[n];Ge=l,gm(l,e)}hm(e)}if(e.subtreeFlags&10256)for(e=e.child;e!==null;)ym(e),e=e.sibling}function ym(e){switch(e.tag){case 0:case 11:case 15:uo(e),e.flags&2048&&ul(9,e,e.return);break;case 3:uo(e);break;case 12:uo(e);break;case 22:var t=e.stateNode;e.memoizedState!==null&&t._visibility&2&&(e.return===null||e.return.tag!==13)?(t._visibility&=-3,Pi(e)):uo(e);break;default:uo(e)}}function Pi(e){var t=e.deletions;if((e.flags&16)!==0){if(t!==null)for(var n=0;n<t.length;n++){var l=t[n];Ge=l,gm(l,e)}hm(e)}for(e=e.child;e!==null;){switch(t=e,t.tag){case 0:case 11:case 15:ul(8,t,t.return),Pi(t);break;case 22:n=t.stateNode,n._visibility&2&&(n._visibility&=-3,Pi(t));break;default:Pi(t)}e=e.sibling}}function gm(e,t){for(;Ge!==null;){var n=Ge;switch(n.tag){case 0:case 11:case 15:ul(8,n,t);break;case 23:case 22:if(n.memoizedState!==null&&n.memoizedState.cachePool!==null){var l=n.memoizedState.cachePool.pool;l!=null&&l.refCount++}break;case 24:Wo(n.memoizedState.cache)}if(l=n.child,l!==null)l.return=n,Ge=l;else e:for(n=e;Ge!==null;){l=Ge;var a=l.sibling,o=l.return;if(sm(l),l===n){Ge=null;break e}if(a!==null){a.return=o,Ge=a;break e}Ge=o}}}var Wh={getCacheForType:function(e){var t=Fe(Xe),n=t.data.get(e);return n===void 0&&(n=e(),t.data.set(e,n)),n},cacheSignal:function(){return Fe(Xe).controller.signal}},Ih=typeof WeakMap=="function"?WeakMap:Map,ue=0,ge=null,te=null,ae=0,de=0,vt=null,Kn=!1,Ua=!1,ed=!1,Ln=0,Ne=0,cl=0,Al=0,td=0,Ct=0,za=0,ko=null,_t=null,er=!1,$s=0,pm=0,Ss=1/0,xs=null,tl=null,qe=0,nl=null,Na=null,kn=0,tr=0,nr=null,bm=null,Mo=0,lr=null;function kt(){return(ue&2)!==0&&ae!==0?ae&-ae:j.T!==null?ld():M1()}function vm(){if(Ct===0)if((ae&536870912)===0||ie){var e=ki;ki<<=1,(ki&3932160)===0&&(ki=262144),Ct=e}else Ct=536870912;return e=At.current,e!==null&&(e.flags|=32),Ct}function ft(e,t,n){(e===ge&&(de===2||de===9)||e.cancelPendingCommit!==null)&&(La(e,0),Jn(e,ae,Ct,!1)),Vo(e,n),((ue&2)===0||e!==ge)&&(e===ge&&((ue&2)===0&&(Al|=n),Ne===4&&Jn(e,ae,Ct,!1)),ln(e))}function Sm(e,t,n){if((ue&6)!==0)throw Error(E(327));var l=!n&&(t&127)===0&&(t&e.expiredLanes)===0||Go(e,t),a=l?ey(e,t):fc(e,t,!0),o=l;do{if(a===0){Ua&&!l&&Jn(e,t,0,!1);break}else{if(n=e.current.alternate,o&&!Fh(n)){a=fc(e,t,!1),o=!1;continue}if(a===2){if(o=t,e.errorRecoveryDisabledLanes&o)var i=0;else i=e.pendingLanes&-536870913,i=i!==0?i:i&536870912?536870912:0;if(i!==0){t=i;e:{var s=e;a=ko;var u=s.current.memoizedState.isDehydrated;if(u&&(La(s,i).flags|=256),i=fc(s,i,!1),i!==2){if(ed&&!u){s.errorRecoveryDisabledLanes|=o,Al|=o,a=4;break e}o=_t,_t=a,o!==null&&(_t===null?_t=o:_t.push.apply(_t,o))}a=i}if(o=!1,a!==2)continue}}if(a===1){La(e,0),Jn(e,t,0,!0);break}e:{switch(l=e,o=a,o){case 0:case 1:throw Error(E(345));case 4:if((t&4194048)!==t)break;case 6:Jn(l,t,Ct,!Kn);break e;case 2:_t=null;break;case 3:case 5:break;default:throw Error(E(329))}if((t&62914560)===t&&(a=$s+300-wt(),10<a)){if(Jn(l,t,Ct,!Kn),Os(l,0,!0)!==0)break e;kn=t,l.timeoutHandle=Xm(Uf.bind(null,l,n,_t,xs,er,t,Ct,Al,za,Kn,o,"Throttled",-0,0),a);break e}Uf(l,n,_t,xs,er,t,Ct,Al,za,Kn,o,null,-0,0)}}break}while(!0);ln(e)}function Uf(e,t,n,l,a,o,i,s,u,h,y,S,p,b){if(e.timeoutHandle=-1,S=t.subtreeFlags,S&8192||(S&16785408)===16785408){S={stylesheets:null,count:0,imgCount:0,imgBytes:0,suspenseyImages:[],waitingForImages:!0,waitingForViewTransition:!1,unsuspend:Cn},mm(t,o,S);var A=(o&62914560)===o?$s-wt():(o&4194048)===o?pm-wt():0;if(A=Dy(S,A),A!==null){kn=o,e.cancelPendingCommit=A(Xf.bind(null,e,t,o,n,l,a,i,s,u,y,S,null,p,b)),Jn(e,o,i,!h);return}}Xf(e,t,o,n,l,a,i,s,u)}function Fh(e){for(var t=e;;){var n=t.tag;if((n===0||n===11||n===15)&&t.flags&16384&&(n=t.updateQueue,n!==null&&(n=n.stores,n!==null)))for(var l=0;l<n.length;l++){var a=n[l],o=a.getSnapshot;a=a.value;try{if(!Mt(o(),a))return!1}catch{return!1}}if(n=t.child,t.subtreeFlags&16384&&n!==null)n.return=t,t=n;else{if(t===e)break;for(;t.sibling===null;){if(t.return===null||t.return===e)return!0;t=t.return}t.sibling.return=t.return,t=t.sibling}}return!0}function Jn(e,t,n,l){t&=~td,t&=~Al,e.suspendedLanes|=t,e.pingedLanes&=~t,l&&(e.warmLanes|=t),l=e.expirationTimes;for(var a=t;0<a;){var o=31-Tt(a),i=1<<o;l[o]=-1,a&=~i}n!==0&&E1(e,n,t)}function Zs(){return(ue&6)===0?(Po(0,!1),!1):!0}function nd(){if(te!==null){if(de===0)var e=te.return;else e=te,wn=Ul=null,Xr(e),Sa=null,Ho=0,e=te;for(;e!==null;)em(e.alternate,e),e=e.return;te=null}}function La(e,t){var n=e.timeoutHandle;n!==-1&&(e.timeoutHandle=-1,yy(n)),n=e.cancelPendingCommit,n!==null&&(e.cancelPendingCommit=null,n()),kn=0,nd(),ge=e,te=n=En(e.current,null),ae=t,de=0,vt=null,Kn=!1,Ua=Go(e,t),ed=!1,za=Ct=td=Al=cl=Ne=0,_t=ko=null,er=!1,(t&8)!==0&&(t|=t&32);var l=e.entangledLanes;if(l!==0)for(e=e.entanglements,l&=t;0<l;){var a=31-Tt(l),o=1<<a;t|=e[a],l&=~o}return Ln=t,Ys(),n}function xm(e,t){J=null,j.H=Ro,t===Ra||t===Us?(t=gf(),de=3):t===Dr?(t=gf(),de=4):de=t===Wr?8:t!==null&&typeof t=="object"&&typeof t.then=="function"?6:1,vt=t,te===null&&(Ne=1,ps(e,Ht(t,e.current)))}function Cm(){var e=At.current;return e===null?!0:(ae&4194048)===ae?Rt===null:(ae&62914560)===ae||(ae&536870912)!==0?e===Rt:!1}function wm(){var e=j.H;return j.H=Ro,e===null?Ro:e}function Em(){var e=j.A;return j.A=Wh,e}function Cs(){Ne=4,Kn||(ae&4194048)!==ae&&At.current!==null||(Ua=!0),(cl&134217727)===0&&(Al&134217727)===0||ge===null||Jn(ge,ae,Ct,!1)}function fc(e,t,n){var l=ue;ue|=2;var a=wm(),o=Em();(ge!==e||ae!==t)&&(xs=null,La(e,t)),t=!1;var i=Ne;e:do try{if(de!==0&&te!==null){var s=te,u=vt;switch(de){case 8:nd(),i=6;break e;case 3:case 2:case 9:case 6:At.current===null&&(t=!0);var h=de;if(de=0,vt=null,ya(e,s,u,h),n&&Ua){i=0;break e}break;default:h=de,de=0,vt=null,ya(e,s,u,h)}}Ph(),i=Ne;break}catch(y){xm(e,y)}while(!0);return t&&e.shellSuspendCounter++,wn=Ul=null,ue=l,j.H=a,j.A=o,te===null&&(ge=null,ae=0,Ys()),i}function Ph(){for(;te!==null;)Tm(te)}function ey(e,t){var n=ue;ue|=2;var l=wm(),a=Em();ge!==e||ae!==t?(xs=null,Ss=wt()+500,La(e,t)):Ua=Go(e,t);e:do try{if(de!==0&&te!==null){t=te;var o=vt;t:switch(de){case 1:de=0,vt=null,ya(e,t,o,1);break;case 2:case 9:if(yf(o)){de=0,vt=null,jf(t);break}t=function(){de!==2&&de!==9||ge!==e||(de=7),ln(e)},o.then(t,t);break e;case 3:de=7;break e;case 4:de=5;break e;case 7:yf(o)?(de=0,vt=null,jf(t)):(de=0,vt=null,ya(e,t,o,7));break;case 5:var i=null;switch(te.tag){case 26:i=te.memoizedState;case 5:case 27:var s=te;if(i?Gm(i):s.stateNode.complete){de=0,vt=null;var u=s.sibling;if(u!==null)te=u;else{var h=s.return;h!==null?(te=h,Gs(h)):te=null}break t}}de=0,vt=null,ya(e,t,o,5);break;case 6:de=0,vt=null,ya(e,t,o,6);break;case 8:nd(),Ne=6;break e;default:throw Error(E(462))}}ty();break}catch(y){xm(e,y)}while(!0);return wn=Ul=null,j.H=l,j.A=a,ue=n,te!==null?0:(ge=null,ae=0,Ys(),Ne)}function ty(){for(;te!==null&&!w2();)Tm(te)}function Tm(e){var t=P0(e.alternate,e,Ln);e.memoizedProps=e.pendingProps,t===null?Gs(e):te=t}function jf(e){var t=e,n=t.alternate;switch(t.tag){case 15:case 0:t=Of(n,t,t.pendingProps,t.type,void 0,ae);break;case 11:t=Of(n,t,t.pendingProps,t.type.render,t.ref,ae);break;case 5:Xr(t);default:em(n,t),t=te=e0(t,Ln),t=P0(n,t,Ln)}e.memoizedProps=e.pendingProps,t===null?Gs(e):te=t}function ya(e,t,n,l){wn=Ul=null,Xr(t),Sa=null,Ho=0;var a=t.return;try{if(qh(e,a,t,n,ae)){Ne=1,ps(e,Ht(n,e.current)),te=null;return}}catch(o){if(a!==null)throw te=a,o;Ne=1,ps(e,Ht(n,e.current)),te=null;return}t.flags&32768?(ie||l===1?e=!0:Ua||(ae&536870912)!==0?e=!1:(Kn=e=!0,(l===2||l===9||l===3||l===6)&&(l=At.current,l!==null&&l.tag===13&&(l.flags|=16384))),km(t,e)):Gs(t)}function Gs(e){var t=e;do{if((t.flags&32768)!==0){km(t,Kn);return}e=t.return;var n=Gh(t.alternate,t,Ln);if(n!==null){te=n;return}if(t=t.sibling,t!==null){te=t;return}te=t=e}while(t!==null);Ne===0&&(Ne=5)}function km(e,t){do{var n=Vh(e.alternate,e);if(n!==null){n.flags&=32767,te=n;return}if(n=e.return,n!==null&&(n.flags|=32768,n.subtreeFlags=0,n.deletions=null),!t&&(e=e.sibling,e!==null)){te=e;return}te=e=n}while(e!==null);Ne=6,te=null}function Xf(e,t,n,l,a,o,i,s,u){e.cancelPendingCommit=null;do Vs();while(qe!==0);if((ue&6)!==0)throw Error(E(327));if(t!==null){if(t===e.current)throw Error(E(177));if(o=t.lanes|t.childLanes,o|=kr,D2(e,n,o,i,s,u),e===ge&&(te=ge=null,ae=0),Na=t,nl=e,kn=n,tr=o,nr=a,bm=l,(t.subtreeFlags&10256)!==0||(t.flags&10256)!==0?(e.callbackNode=null,e.callbackPriority=0,oy(ss,function(){return Lm(),null})):(e.callbackNode=null,e.callbackPriority=0),l=(t.flags&13878)!==0,(t.subtreeFlags&13878)!==0||l){l=j.T,j.T=null,a=ce.p,ce.p=2,i=ue,ue|=4;try{Kh(e,t,n)}finally{ue=i,ce.p=a,j.T=l}}qe=1,Mm(),Am(),zm()}}function Mm(){if(qe===1){qe=0;var e=nl,t=Na,n=(t.flags&13878)!==0;if((t.subtreeFlags&13878)!==0||n){n=j.T,j.T=null;var l=ce.p;ce.p=2;var a=ue;ue|=4;try{dm(t,e);var o=sr,i=G1(e.containerInfo),s=o.focusedElem,u=o.selectionRange;if(i!==s&&s&&s.ownerDocument&&Z1(s.ownerDocument.documentElement,s)){if(u!==null&&Tr(s)){var h=u.start,y=u.end;if(y===void 0&&(y=h),"selectionStart"in s)s.selectionStart=h,s.selectionEnd=Math.min(y,s.value.length);else{var S=s.ownerDocument||document,p=S&&S.defaultView||window;if(p.getSelection){var b=p.getSelection(),A=s.textContent.length,k=Math.min(u.start,A),G=u.end===void 0?k:Math.min(u.end,A);!b.extend&&k>G&&(i=G,G=k,k=i);var f=cf(s,k),_=cf(s,G);if(f&&_&&(b.rangeCount!==1||b.anchorNode!==f.node||b.anchorOffset!==f.offset||b.focusNode!==_.node||b.focusOffset!==_.offset)){var g=S.createRange();g.setStart(f.node,f.offset),b.removeAllRanges(),k>G?(b.addRange(g),b.extend(_.node,_.offset)):(g.setEnd(_.node,_.offset),b.addRange(g))}}}}for(S=[],b=s;b=b.parentNode;)b.nodeType===1&&S.push({element:b,left:b.scrollLeft,top:b.scrollTop});for(typeof s.focus=="function"&&s.focus(),s=0;s<S.length;s++){var x=S[s];x.element.scrollLeft=x.left,x.element.scrollTop=x.top}}Ns=!!ir,sr=ir=null}finally{ue=a,ce.p=l,j.T=n}}e.current=t,qe=2}}function Am(){if(qe===2){qe=0;var e=nl,t=Na,n=(t.flags&8772)!==0;if((t.subtreeFlags&8772)!==0||n){n=j.T,j.T=null;var l=ce.p;ce.p=2;var a=ue;ue|=4;try{im(e,t.alternate,t)}finally{ue=a,ce.p=l,j.T=n}}qe=3}}function zm(){if(qe===4||qe===3){qe=0,E2();var e=nl,t=Na,n=kn,l=bm;(t.subtreeFlags&10256)!==0||(t.flags&10256)!==0?qe=5:(qe=0,Na=nl=null,Nm(e,e.pendingLanes));var a=e.pendingLanes;if(a===0&&(tl=null),br(n),t=t.stateNode,Et&&typeof Et.onCommitFiberRoot=="function")try{Et.onCommitFiberRoot(Zo,t,void 0,(t.current.flags&128)===128)}catch{}if(l!==null){t=j.T,a=ce.p,ce.p=2,j.T=null;try{for(var o=e.onRecoverableError,i=0;i<l.length;i++){var s=l[i];o(s.value,{componentStack:s.stack})}}finally{j.T=t,ce.p=a}}(kn&3)!==0&&Vs(),ln(e),a=e.pendingLanes,(n&261930)!==0&&(a&42)!==0?e===lr?Mo++:(Mo=0,lr=e):Mo=0,Po(0,!1)}}function Nm(e,t){(e.pooledCacheLanes&=t)===0&&(t=e.pooledCache,t!=null&&(e.pooledCache=null,Wo(t)))}function Vs(){return Mm(),Am(),zm(),Lm()}function Lm(){if(qe!==5)return!1;var e=nl,t=tr;tr=0;var n=br(kn),l=j.T,a=ce.p;try{ce.p=32>n?32:n,j.T=null,n=nr,nr=null;var o=nl,i=kn;if(qe=0,Na=nl=null,kn=0,(ue&6)!==0)throw Error(E(331));var s=ue;if(ue|=4,ym(o.current),fm(o,o.current,i,n),ue=s,Po(0,!1),Et&&typeof Et.onPostCommitFiberRoot=="function")try{Et.onPostCommitFiberRoot(Zo,o)}catch{}return!0}finally{ce.p=a,j.T=l,Nm(e,t)}}function Qf(e,t,n){t=Ht(n,t),t=Wc(e.stateNode,t,2),e=el(e,t,2),e!==null&&(Vo(e,2),ln(e))}function _e(e,t,n){if(e.tag===3)Qf(e,e,n);else for(;t!==null;){if(t.tag===3){Qf(t,e,n);break}else if(t.tag===1){var l=t.stateNode;if(typeof t.type.getDerivedStateFromError=="function"||typeof l.componentDidCatch=="function"&&(tl===null||!tl.has(l))){e=Ht(n,e),n=V0(2),l=el(t,n,2),l!==null&&(K0(n,l,t,e),Vo(l,2),ln(l));break}}t=t.return}}function mc(e,t,n){var l=e.pingCache;if(l===null){l=e.pingCache=new Ih;var a=new Set;l.set(t,a)}else a=l.get(t),a===void 0&&(a=new Set,l.set(t,a));a.has(n)||(ed=!0,a.add(n),e=ny.bind(null,e,t,n),t.then(e,e))}function ny(e,t,n){var l=e.pingCache;l!==null&&l.delete(t),e.pingedLanes|=e.suspendedLanes&n,e.warmLanes&=~n,ge===e&&(ae&n)===n&&(Ne===4||Ne===3&&(ae&62914560)===ae&&300>wt()-$s?(ue&2)===0&&La(e,0):td|=n,za===ae&&(za=0)),ln(e)}function Om(e,t){t===0&&(t=w1()),e=Rl(e,t),e!==null&&(Vo(e,t),ln(e))}function ly(e){var t=e.memoizedState,n=0;t!==null&&(n=t.retryLane),Om(e,n)}function ay(e,t){var n=0;switch(e.tag){case 31:case 13:var l=e.stateNode,a=e.memoizedState;a!==null&&(n=a.retryLane);break;case 19:l=e.stateNode;break;case 22:l=e.stateNode._retryCache;break;default:throw Error(E(314))}l!==null&&l.delete(t),Om(e,n)}function oy(e,t){return gr(e,t)}var ws=null,aa=null,ar=!1,Es=!1,hc=!1,Wn=0;function ln(e){e!==aa&&e.next===null&&(aa===null?ws=aa=e:aa=aa.next=e),Es=!0,ar||(ar=!0,sy())}function Po(e,t){if(!hc&&Es){hc=!0;do for(var n=!1,l=ws;l!==null;){if(!t)if(e!==0){var a=l.pendingLanes;if(a===0)var o=0;else{var i=l.suspendedLanes,s=l.pingedLanes;o=(1<<31-Tt(42|e)+1)-1,o&=a&~(i&~s),o=o&201326741?o&201326741|1:o?o|2:0}o!==0&&(n=!0,qf(l,o))}else o=ae,o=Os(l,l===ge?o:0,l.cancelPendingCommit!==null||l.timeoutHandle!==-1),(o&3)===0||Go(l,o)||(n=!0,qf(l,o));l=l.next}while(n);hc=!1}}function iy(){Dm()}function Dm(){Es=ar=!1;var e=0;Wn!==0&&hy()&&(e=Wn);for(var t=wt(),n=null,l=ws;l!==null;){var a=l.next,o=Bm(l,t);o===0?(l.next=null,n===null?ws=a:n.next=a,a===null&&(aa=n)):(n=l,(e!==0||(o&3)!==0)&&(Es=!0)),l=a}qe!==0&&qe!==5||Po(e,!1),Wn!==0&&(Wn=0)}function Bm(e,t){for(var n=e.suspendedLanes,l=e.pingedLanes,a=e.expirationTimes,o=e.pendingLanes&-62914561;0<o;){var i=31-Tt(o),s=1<<i,u=a[i];u===-1?((s&n)===0||(s&l)!==0)&&(a[i]=O2(s,t)):u<=t&&(e.expiredLanes|=s),o&=~s}if(t=ge,n=ae,n=Os(e,e===t?n:0,e.cancelPendingCommit!==null||e.timeoutHandle!==-1),l=e.callbackNode,n===0||e===t&&(de===2||de===9)||e.cancelPendingCommit!==null)return l!==null&&l!==null&&$u(l),e.callbackNode=null,e.callbackPriority=0;if((n&3)===0||Go(e,n)){if(t=n&-n,t===e.callbackPriority)return t;switch(l!==null&&$u(l),br(n)){case 2:case 8:n=x1;break;case 32:n=ss;break;case 268435456:n=C1;break;default:n=ss}return l=Hm.bind(null,e),n=gr(n,l),e.callbackPriority=t,e.callbackNode=n,t}return l!==null&&l!==null&&$u(l),e.callbackPriority=2,e.callbackNode=null,2}function Hm(e,t){if(qe!==0&&qe!==5)return e.callbackNode=null,e.callbackPriority=0,null;var n=e.callbackNode;if(Vs()&&e.callbackNode!==n)return null;var l=ae;return l=Os(e,e===ge?l:0,e.cancelPendingCommit!==null||e.timeoutHandle!==-1),l===0?null:(Sm(e,l,t),Bm(e,wt()),e.callbackNode!=null&&e.callbackNode===n?Hm.bind(null,e):null)}function qf(e,t){if(Vs())return null;Sm(e,t,!0)}function sy(){gy(function(){(ue&6)!==0?gr(S1,iy):Dm()})}function ld(){if(Wn===0){var e=ka;e===0&&(e=Ti,Ti<<=1,(Ti&261888)===0&&(Ti=256)),Wn=e}return Wn}function $f(e){return e==null||typeof e=="symbol"||typeof e=="boolean"?null:typeof e=="function"?e:$i(""+e)}function Zf(e,t){var n=t.ownerDocument.createElement("input");return n.name=t.name,n.value=t.value,e.id&&n.setAttribute("form",e.id),t.parentNode.insertBefore(n,t),e=new FormData(e),n.parentNode.removeChild(n),e}function uy(e,t,n,l,a){if(t==="submit"&&n&&n.stateNode===a){var o=$f((a[mt]||null).action),i=l.submitter;i&&(t=(t=i[mt]||null)?$f(t.formAction):i.getAttribute("formAction"),t!==null&&(o=t,i=null));var s=new Ds("action","action",null,l,a);e.push({event:s,listeners:[{instance:null,listener:function(){if(l.defaultPrevented){if(Wn!==0){var u=i?Zf(a,i):new FormData(a);Kc(n,{pending:!0,data:u,method:a.method,action:o},null,u)}}else typeof o=="function"&&(s.preventDefault(),u=i?Zf(a,i):new FormData(a),Kc(n,{pending:!0,data:u,method:a.method,action:o},o,u))},currentTarget:a}]})}}for(Ri=0;Ri<Hc.length;Ri++)Ui=Hc[Ri],Gf=Ui.toLowerCase(),Vf=Ui[0].toUpperCase()+Ui.slice(1),Zt(Gf,"on"+Vf);var Ui,Gf,Vf,Ri;Zt(K1,"onAnimationEnd");Zt(J1,"onAnimationIteration");Zt(W1,"onAnimationStart");Zt("dblclick","onDoubleClick");Zt("focusin","onFocus");Zt("focusout","onBlur");Zt(Th,"onTransitionRun");Zt(kh,"onTransitionStart");Zt(Mh,"onTransitionCancel");Zt(I1,"onTransitionEnd");Ea("onMouseEnter",["mouseout","mouseover"]);Ea("onMouseLeave",["mouseout","mouseover"]);Ea("onPointerEnter",["pointerout","pointerover"]);Ea("onPointerLeave",["pointerout","pointerover"]);Bl("onChange","change click focusin focusout input keydown keyup selectionchange".split(" "));Bl("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" "));Bl("onBeforeInput",["compositionend","keypress","textInput","paste"]);Bl("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" "));Bl("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" "));Bl("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var Uo="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),cy=new Set("beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(Uo));function Ym(e,t){t=(t&4)!==0;for(var n=0;n<e.length;n++){var l=e[n],a=l.event;l=l.listeners;e:{var o=void 0;if(t)for(var i=l.length-1;0<=i;i--){var s=l[i],u=s.instance,h=s.currentTarget;if(s=s.listener,u!==o&&a.isPropagationStopped())break e;o=s,a.currentTarget=h;try{o(a)}catch(y){cs(y)}a.currentTarget=null,o=u}else for(i=0;i<l.length;i++){if(s=l[i],u=s.instance,h=s.currentTarget,s=s.listener,u!==o&&a.isPropagationStopped())break e;o=s,a.currentTarget=h;try{o(a)}catch(y){cs(y)}a.currentTarget=null,o=u}}}}function ee(e,t){var n=t[Mc];n===void 0&&(n=t[Mc]=new Set);var l=e+"__bubble";n.has(l)||(Rm(t,e,2,!1),n.add(l))}function yc(e,t,n){var l=0;t&&(l|=4),Rm(n,e,l,t)}var ji="_reactListening"+Math.random().toString(36).slice(2);function ad(e){if(!e[ji]){e[ji]=!0,A1.forEach(function(n){n!=="selectionchange"&&(cy.has(n)||yc(n,!1,e),yc(n,!0,e))});var t=e.nodeType===9?e:e.ownerDocument;t===null||t[ji]||(t[ji]=!0,yc("selectionchange",!1,t))}}function Rm(e,t,n,l){switch(Im(t)){case 2:var a=Yy;break;case 8:a=Ry;break;default:a=ud}n=a.bind(null,t,n,e),a=void 0,!Oc||t!=="touchstart"&&t!=="touchmove"&&t!=="wheel"||(a=!0),l?a!==void 0?e.addEventListener(t,n,{capture:!0,passive:a}):e.addEventListener(t,n,!0):a!==void 0?e.addEventListener(t,n,{passive:a}):e.addEventListener(t,n,!1)}function gc(e,t,n,l,a){var o=l;if((t&1)===0&&(t&2)===0&&l!==null)e:for(;;){if(l===null)return;var i=l.tag;if(i===3||i===4){var s=l.stateNode.containerInfo;if(s===a)break;if(i===4)for(i=l.return;i!==null;){var u=i.tag;if((u===3||u===4)&&i.stateNode.containerInfo===a)return;i=i.return}for(;s!==null;){if(i=sa(s),i===null)return;if(u=i.tag,u===5||u===6||u===26||u===27){l=o=i;continue e}s=s.parentNode}}l=l.return}Y1(function(){var h=o,y=xr(n),S=[];e:{var p=F1.get(e);if(p!==void 0){var b=Ds,A=e;switch(e){case"keypress":if(Gi(n)===0)break e;case"keydown":case"keyup":b=ah;break;case"focusin":A="focus",b=Ju;break;case"focusout":A="blur",b=Ju;break;case"beforeblur":case"afterblur":b=Ju;break;case"click":if(n.button===2)break e;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":b=P_;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":b=G2;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":b=sh;break;case K1:case J1:case W1:b=J2;break;case I1:b=ch;break;case"scroll":case"scrollend":b=$2;break;case"wheel":b=dh;break;case"copy":case"cut":case"paste":b=I2;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":b=tf;break;case"toggle":case"beforetoggle":b=fh}var k=(t&4)!==0,G=!k&&(e==="scroll"||e==="scrollend"),f=k?p!==null?p+"Capture":null:p;k=[];for(var _=h,g;_!==null;){var x=_;if(g=x.stateNode,x=x.tag,x!==5&&x!==26&&x!==27||g===null||f===null||(x=No(_,f),x!=null&&k.push(jo(_,x,g))),G)break;_=_.return}0<k.length&&(p=new b(p,A,null,n,y),S.push({event:p,listeners:k}))}}if((t&7)===0){e:{if(p=e==="mouseover"||e==="pointerover",b=e==="mouseout"||e==="pointerout",p&&n!==Lc&&(A=n.relatedTarget||n.fromElement)&&(sa(A)||A[Ba]))break e;if((b||p)&&(p=y.window===y?y:(p=y.ownerDocument)?p.defaultView||p.parentWindow:window,b?(A=n.relatedTarget||n.toElement,b=h,A=A?sa(A):null,A!==null&&(G=$o(A),k=A.tag,A!==G||k!==5&&k!==27&&k!==6)&&(A=null)):(b=null,A=h),b!==A)){if(k=P_,x="onMouseLeave",f="onMouseEnter",_="mouse",(e==="pointerout"||e==="pointerover")&&(k=tf,x="onPointerLeave",f="onPointerEnter",_="pointer"),G=b==null?p:mo(b),g=A==null?p:mo(A),p=new k(x,_+"leave",b,n,y),p.target=G,p.relatedTarget=g,x=null,sa(y)===h&&(k=new k(f,_+"enter",A,n,y),k.target=g,k.relatedTarget=G,x=k),G=x,b&&A)t:{for(k=ry,f=b,_=A,g=0,x=f;x;x=k(x))g++;x=0;for(var O=_;O;O=k(O))x++;for(;0<g-x;)f=k(f),g--;for(;0<x-g;)_=k(_),x--;for(;g--;){if(f===_||_!==null&&f===_.alternate){k=f;break t}f=k(f),_=k(_)}k=null}else k=null;b!==null&&Kf(S,p,b,k,!1),A!==null&&G!==null&&Kf(S,G,A,k,!0)}}e:{if(p=h?mo(h):window,b=p.nodeName&&p.nodeName.toLowerCase(),b==="select"||b==="input"&&p.type==="file")var le=of;else if(af(p))if(q1)le=Ch;else{le=Sh;var L=vh}else b=p.nodeName,!b||b.toLowerCase()!=="input"||p.type!=="checkbox"&&p.type!=="radio"?h&&Sr(h.elementType)&&(le=of):le=xh;if(le&&(le=le(e,h))){Q1(S,le,n,y);break e}L&&L(e,p,h),e==="focusout"&&h&&p.type==="number"&&h.memoizedProps.value!=null&&Nc(p,"number",p.value)}switch(L=h?mo(h):window,e){case"focusin":(af(L)||L.contentEditable==="true")&&(ra=L,Dc=h,bo=null);break;case"focusout":bo=Dc=ra=null;break;case"mousedown":Bc=!0;break;case"contextmenu":case"mouseup":case"dragend":Bc=!1,rf(S,n,y);break;case"selectionchange":if(Eh)break;case"keydown":case"keyup":rf(S,n,y)}var U;if(Er)e:{switch(e){case"compositionstart":var W="onCompositionStart";break e;case"compositionend":W="onCompositionEnd";break e;case"compositionupdate":W="onCompositionUpdate";break e}W=void 0}else ca?j1(e,n)&&(W="onCompositionEnd"):e==="keydown"&&n.keyCode===229&&(W="onCompositionStart");W&&(U1&&n.locale!=="ko"&&(ca||W!=="onCompositionStart"?W==="onCompositionEnd"&&ca&&(U=R1()):(Vn=y,Cr="value"in Vn?Vn.value:Vn.textContent,ca=!0)),L=Ts(h,W),0<L.length&&(W=new ef(W,e,null,n,y),S.push({event:W,listeners:L}),U?W.data=U:(U=X1(n),U!==null&&(W.data=U)))),(U=hh?yh(e,n):gh(e,n))&&(W=Ts(h,"onBeforeInput"),0<W.length&&(L=new ef("onBeforeInput","beforeinput",null,n,y),S.push({event:L,listeners:W}),L.data=U)),uy(S,e,h,n,y)}Ym(S,t)})}function jo(e,t,n){return{instance:e,listener:t,currentTarget:n}}function Ts(e,t){for(var n=t+"Capture",l=[];e!==null;){var a=e,o=a.stateNode;if(a=a.tag,a!==5&&a!==26&&a!==27||o===null||(a=No(e,n),a!=null&&l.unshift(jo(e,a,o)),a=No(e,t),a!=null&&l.push(jo(e,a,o))),e.tag===3)return l;e=e.return}return[]}function ry(e){if(e===null)return null;do e=e.return;while(e&&e.tag!==5&&e.tag!==27);return e||null}function Kf(e,t,n,l,a){for(var o=t._reactName,i=[];n!==null&&n!==l;){var s=n,u=s.alternate,h=s.stateNode;if(s=s.tag,u!==null&&u===l)break;s!==5&&s!==26&&s!==27||h===null||(u=h,a?(h=No(n,o),h!=null&&i.unshift(jo(n,h,u))):a||(h=No(n,o),h!=null&&i.push(jo(n,h,u)))),n=n.return}i.length!==0&&e.push({event:t,listeners:i})}var dy=/\r\n?/g,_y=/\u0000|\uFFFD/g;function Jf(e){return(typeof e=="string"?e:""+e).replace(dy,`
`).replace(_y,"")}function Um(e,t){return t=Jf(t),Jf(e)===t}function fe(e,t,n,l,a,o){switch(n){case"children":typeof l=="string"?t==="body"||t==="textarea"&&l===""||Ta(e,l):(typeof l=="number"||typeof l=="bigint")&&t!=="body"&&Ta(e,""+l);break;case"className":Ai(e,"class",l);break;case"tabIndex":Ai(e,"tabindex",l);break;case"dir":case"role":case"viewBox":case"width":case"height":Ai(e,n,l);break;case"style":H1(e,l,o);break;case"data":if(t!=="object"){Ai(e,"data",l);break}case"src":case"href":if(l===""&&(t!=="a"||n!=="href")){e.removeAttribute(n);break}if(l==null||typeof l=="function"||typeof l=="symbol"||typeof l=="boolean"){e.removeAttribute(n);break}l=$i(""+l),e.setAttribute(n,l);break;case"action":case"formAction":if(typeof l=="function"){e.setAttribute(n,"javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')");break}else typeof o=="function"&&(n==="formAction"?(t!=="input"&&fe(e,t,"name",a.name,a,null),fe(e,t,"formEncType",a.formEncType,a,null),fe(e,t,"formMethod",a.formMethod,a,null),fe(e,t,"formTarget",a.formTarget,a,null)):(fe(e,t,"encType",a.encType,a,null),fe(e,t,"method",a.method,a,null),fe(e,t,"target",a.target,a,null)));if(l==null||typeof l=="symbol"||typeof l=="boolean"){e.removeAttribute(n);break}l=$i(""+l),e.setAttribute(n,l);break;case"onClick":l!=null&&(e.onclick=Cn);break;case"onScroll":l!=null&&ee("scroll",e);break;case"onScrollEnd":l!=null&&ee("scrollend",e);break;case"dangerouslySetInnerHTML":if(l!=null){if(typeof l!="object"||!("__html"in l))throw Error(E(61));if(n=l.__html,n!=null){if(a.children!=null)throw Error(E(60));e.innerHTML=n}}break;case"multiple":e.multiple=l&&typeof l!="function"&&typeof l!="symbol";break;case"muted":e.muted=l&&typeof l!="function"&&typeof l!="symbol";break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"defaultValue":case"defaultChecked":case"innerHTML":case"ref":break;case"autoFocus":break;case"xlinkHref":if(l==null||typeof l=="function"||typeof l=="boolean"||typeof l=="symbol"){e.removeAttribute("xlink:href");break}n=$i(""+l),e.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",n);break;case"contentEditable":case"spellCheck":case"draggable":case"value":case"autoReverse":case"externalResourcesRequired":case"focusable":case"preserveAlpha":l!=null&&typeof l!="function"&&typeof l!="symbol"?e.setAttribute(n,""+l):e.removeAttribute(n);break;case"inert":case"allowFullScreen":case"async":case"autoPlay":case"controls":case"default":case"defer":case"disabled":case"disablePictureInPicture":case"disableRemotePlayback":case"formNoValidate":case"hidden":case"loop":case"noModule":case"noValidate":case"open":case"playsInline":case"readOnly":case"required":case"reversed":case"scoped":case"seamless":case"itemScope":l&&typeof l!="function"&&typeof l!="symbol"?e.setAttribute(n,""):e.removeAttribute(n);break;case"capture":case"download":l===!0?e.setAttribute(n,""):l!==!1&&l!=null&&typeof l!="function"&&typeof l!="symbol"?e.setAttribute(n,l):e.removeAttribute(n);break;case"cols":case"rows":case"size":case"span":l!=null&&typeof l!="function"&&typeof l!="symbol"&&!isNaN(l)&&1<=l?e.setAttribute(n,l):e.removeAttribute(n);break;case"rowSpan":case"start":l==null||typeof l=="function"||typeof l=="symbol"||isNaN(l)?e.removeAttribute(n):e.setAttribute(n,l);break;case"popover":ee("beforetoggle",e),ee("toggle",e),qi(e,"popover",l);break;case"xlinkActuate":hn(e,"http://www.w3.org/1999/xlink","xlink:actuate",l);break;case"xlinkArcrole":hn(e,"http://www.w3.org/1999/xlink","xlink:arcrole",l);break;case"xlinkRole":hn(e,"http://www.w3.org/1999/xlink","xlink:role",l);break;case"xlinkShow":hn(e,"http://www.w3.org/1999/xlink","xlink:show",l);break;case"xlinkTitle":hn(e,"http://www.w3.org/1999/xlink","xlink:title",l);break;case"xlinkType":hn(e,"http://www.w3.org/1999/xlink","xlink:type",l);break;case"xmlBase":hn(e,"http://www.w3.org/XML/1998/namespace","xml:base",l);break;case"xmlLang":hn(e,"http://www.w3.org/XML/1998/namespace","xml:lang",l);break;case"xmlSpace":hn(e,"http://www.w3.org/XML/1998/namespace","xml:space",l);break;case"is":qi(e,"is",l);break;case"innerText":case"textContent":break;default:(!(2<n.length)||n[0]!=="o"&&n[0]!=="O"||n[1]!=="n"&&n[1]!=="N")&&(n=Q2.get(n)||n,qi(e,n,l))}}function or(e,t,n,l,a,o){switch(n){case"style":H1(e,l,o);break;case"dangerouslySetInnerHTML":if(l!=null){if(typeof l!="object"||!("__html"in l))throw Error(E(61));if(n=l.__html,n!=null){if(a.children!=null)throw Error(E(60));e.innerHTML=n}}break;case"children":typeof l=="string"?Ta(e,l):(typeof l=="number"||typeof l=="bigint")&&Ta(e,""+l);break;case"onScroll":l!=null&&ee("scroll",e);break;case"onScrollEnd":l!=null&&ee("scrollend",e);break;case"onClick":l!=null&&(e.onclick=Cn);break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"innerHTML":case"ref":break;case"innerText":case"textContent":break;default:if(!z1.hasOwnProperty(n))e:{if(n[0]==="o"&&n[1]==="n"&&(a=n.endsWith("Capture"),t=n.slice(2,a?n.length-7:void 0),o=e[mt]||null,o=o!=null?o[n]:null,typeof o=="function"&&e.removeEventListener(t,o,a),typeof l=="function")){typeof o!="function"&&o!==null&&(n in e?e[n]=null:e.hasAttribute(n)&&e.removeAttribute(n)),e.addEventListener(t,l,a);break e}n in e?e[n]=l:l===!0?e.setAttribute(n,""):qi(e,n,l)}}}function Pe(e,t,n){switch(t){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"img":ee("error",e),ee("load",e);var l=!1,a=!1,o;for(o in n)if(n.hasOwnProperty(o)){var i=n[o];if(i!=null)switch(o){case"src":l=!0;break;case"srcSet":a=!0;break;case"children":case"dangerouslySetInnerHTML":throw Error(E(137,t));default:fe(e,t,o,i,n,null)}}a&&fe(e,t,"srcSet",n.srcSet,n,null),l&&fe(e,t,"src",n.src,n,null);return;case"input":ee("invalid",e);var s=o=i=a=null,u=null,h=null;for(l in n)if(n.hasOwnProperty(l)){var y=n[l];if(y!=null)switch(l){case"name":a=y;break;case"type":i=y;break;case"checked":u=y;break;case"defaultChecked":h=y;break;case"value":o=y;break;case"defaultValue":s=y;break;case"children":case"dangerouslySetInnerHTML":if(y!=null)throw Error(E(137,t));break;default:fe(e,t,l,y,n,null)}}O1(e,o,s,u,h,i,a,!1);return;case"select":ee("invalid",e),l=i=o=null;for(a in n)if(n.hasOwnProperty(a)&&(s=n[a],s!=null))switch(a){case"value":o=s;break;case"defaultValue":i=s;break;case"multiple":l=s;default:fe(e,t,a,s,n,null)}t=o,n=i,e.multiple=!!l,t!=null?pa(e,!!l,t,!1):n!=null&&pa(e,!!l,n,!0);return;case"textarea":ee("invalid",e),o=a=l=null;for(i in n)if(n.hasOwnProperty(i)&&(s=n[i],s!=null))switch(i){case"value":l=s;break;case"defaultValue":a=s;break;case"children":o=s;break;case"dangerouslySetInnerHTML":if(s!=null)throw Error(E(91));break;default:fe(e,t,i,s,n,null)}B1(e,l,a,o);return;case"option":for(u in n)n.hasOwnProperty(u)&&(l=n[u],l!=null)&&(u==="selected"?e.selected=l&&typeof l!="function"&&typeof l!="symbol":fe(e,t,u,l,n,null));return;case"dialog":ee("beforetoggle",e),ee("toggle",e),ee("cancel",e),ee("close",e);break;case"iframe":case"object":ee("load",e);break;case"video":case"audio":for(l=0;l<Uo.length;l++)ee(Uo[l],e);break;case"image":ee("error",e),ee("load",e);break;case"details":ee("toggle",e);break;case"embed":case"source":case"link":ee("error",e),ee("load",e);case"area":case"base":case"br":case"col":case"hr":case"keygen":case"meta":case"param":case"track":case"wbr":case"menuitem":for(h in n)if(n.hasOwnProperty(h)&&(l=n[h],l!=null))switch(h){case"children":case"dangerouslySetInnerHTML":throw Error(E(137,t));default:fe(e,t,h,l,n,null)}return;default:if(Sr(t)){for(y in n)n.hasOwnProperty(y)&&(l=n[y],l!==void 0&&or(e,t,y,l,n,void 0));return}}for(s in n)n.hasOwnProperty(s)&&(l=n[s],l!=null&&fe(e,t,s,l,n,null))}function fy(e,t,n,l){switch(t){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"input":var a=null,o=null,i=null,s=null,u=null,h=null,y=null;for(b in n){var S=n[b];if(n.hasOwnProperty(b)&&S!=null)switch(b){case"checked":break;case"value":break;case"defaultValue":u=S;default:l.hasOwnProperty(b)||fe(e,t,b,null,l,S)}}for(var p in l){var b=l[p];if(S=n[p],l.hasOwnProperty(p)&&(b!=null||S!=null))switch(p){case"type":o=b;break;case"name":a=b;break;case"checked":h=b;break;case"defaultChecked":y=b;break;case"value":i=b;break;case"defaultValue":s=b;break;case"children":case"dangerouslySetInnerHTML":if(b!=null)throw Error(E(137,t));break;default:b!==S&&fe(e,t,p,b,l,S)}}zc(e,i,s,u,h,y,o,a);return;case"select":b=i=s=p=null;for(o in n)if(u=n[o],n.hasOwnProperty(o)&&u!=null)switch(o){case"value":break;case"multiple":b=u;default:l.hasOwnProperty(o)||fe(e,t,o,null,l,u)}for(a in l)if(o=l[a],u=n[a],l.hasOwnProperty(a)&&(o!=null||u!=null))switch(a){case"value":p=o;break;case"defaultValue":s=o;break;case"multiple":i=o;default:o!==u&&fe(e,t,a,o,l,u)}t=s,n=i,l=b,p!=null?pa(e,!!n,p,!1):!!l!=!!n&&(t!=null?pa(e,!!n,t,!0):pa(e,!!n,n?[]:"",!1));return;case"textarea":b=p=null;for(s in n)if(a=n[s],n.hasOwnProperty(s)&&a!=null&&!l.hasOwnProperty(s))switch(s){case"value":break;case"children":break;default:fe(e,t,s,null,l,a)}for(i in l)if(a=l[i],o=n[i],l.hasOwnProperty(i)&&(a!=null||o!=null))switch(i){case"value":p=a;break;case"defaultValue":b=a;break;case"children":break;case"dangerouslySetInnerHTML":if(a!=null)throw Error(E(91));break;default:a!==o&&fe(e,t,i,a,l,o)}D1(e,p,b);return;case"option":for(var A in n)p=n[A],n.hasOwnProperty(A)&&p!=null&&!l.hasOwnProperty(A)&&(A==="selected"?e.selected=!1:fe(e,t,A,null,l,p));for(u in l)p=l[u],b=n[u],l.hasOwnProperty(u)&&p!==b&&(p!=null||b!=null)&&(u==="selected"?e.selected=p&&typeof p!="function"&&typeof p!="symbol":fe(e,t,u,p,l,b));return;case"img":case"link":case"area":case"base":case"br":case"col":case"embed":case"hr":case"keygen":case"meta":case"param":case"source":case"track":case"wbr":case"menuitem":for(var k in n)p=n[k],n.hasOwnProperty(k)&&p!=null&&!l.hasOwnProperty(k)&&fe(e,t,k,null,l,p);for(h in l)if(p=l[h],b=n[h],l.hasOwnProperty(h)&&p!==b&&(p!=null||b!=null))switch(h){case"children":case"dangerouslySetInnerHTML":if(p!=null)throw Error(E(137,t));break;default:fe(e,t,h,p,l,b)}return;default:if(Sr(t)){for(var G in n)p=n[G],n.hasOwnProperty(G)&&p!==void 0&&!l.hasOwnProperty(G)&&or(e,t,G,void 0,l,p);for(y in l)p=l[y],b=n[y],!l.hasOwnProperty(y)||p===b||p===void 0&&b===void 0||or(e,t,y,p,l,b);return}}for(var f in n)p=n[f],n.hasOwnProperty(f)&&p!=null&&!l.hasOwnProperty(f)&&fe(e,t,f,null,l,p);for(S in l)p=l[S],b=n[S],!l.hasOwnProperty(S)||p===b||p==null&&b==null||fe(e,t,S,p,l,b)}function Wf(e){switch(e){case"css":case"script":case"font":case"img":case"image":case"input":case"link":return!0;default:return!1}}function my(){if(typeof performance.getEntriesByType=="function"){for(var e=0,t=0,n=performance.getEntriesByType("resource"),l=0;l<n.length;l++){var a=n[l],o=a.transferSize,i=a.initiatorType,s=a.duration;if(o&&s&&Wf(i)){for(i=0,s=a.responseEnd,l+=1;l<n.length;l++){var u=n[l],h=u.startTime;if(h>s)break;var y=u.transferSize,S=u.initiatorType;y&&Wf(S)&&(u=u.responseEnd,i+=y*(u<s?1:(s-h)/(u-h)))}if(--l,t+=8*(o+i)/(a.duration/1e3),e++,10<e)break}}if(0<e)return t/e/1e6}return navigator.connection&&(e=navigator.connection.downlink,typeof e=="number")?e:5}var ir=null,sr=null;function ks(e){return e.nodeType===9?e:e.ownerDocument}function If(e){switch(e){case"http://www.w3.org/2000/svg":return 1;case"http://www.w3.org/1998/Math/MathML":return 2;default:return 0}}function jm(e,t){if(e===0)switch(t){case"svg":return 1;case"math":return 2;default:return 0}return e===1&&t==="foreignObject"?0:e}function ur(e,t){return e==="textarea"||e==="noscript"||typeof t.children=="string"||typeof t.children=="number"||typeof t.children=="bigint"||typeof t.dangerouslySetInnerHTML=="object"&&t.dangerouslySetInnerHTML!==null&&t.dangerouslySetInnerHTML.__html!=null}var pc=null;function hy(){var e=window.event;return e&&e.type==="popstate"?e===pc?!1:(pc=e,!0):(pc=null,!1)}var Xm=typeof setTimeout=="function"?setTimeout:void 0,yy=typeof clearTimeout=="function"?clearTimeout:void 0,Ff=typeof Promise=="function"?Promise:void 0,gy=typeof queueMicrotask=="function"?queueMicrotask:typeof Ff<"u"?function(e){return Ff.resolve(null).then(e).catch(py)}:Xm;function py(e){setTimeout(function(){throw e})}function dl(e){return e==="head"}function Pf(e,t){var n=t,l=0;do{var a=n.nextSibling;if(e.removeChild(n),a&&a.nodeType===8)if(n=a.data,n==="/$"||n==="/&"){if(l===0){e.removeChild(a),Da(t);return}l--}else if(n==="$"||n==="$?"||n==="$~"||n==="$!"||n==="&")l++;else if(n==="html")Ao(e.ownerDocument.documentElement);else if(n==="head"){n=e.ownerDocument.head,Ao(n);for(var o=n.firstChild;o;){var i=o.nextSibling,s=o.nodeName;o[Ko]||s==="SCRIPT"||s==="STYLE"||s==="LINK"&&o.rel.toLowerCase()==="stylesheet"||n.removeChild(o),o=i}}else n==="body"&&Ao(e.ownerDocument.body);n=a}while(n);Da(t)}function e1(e,t){var n=e;e=0;do{var l=n.nextSibling;if(n.nodeType===1?t?(n._stashedDisplay=n.style.display,n.style.display="none"):(n.style.display=n._stashedDisplay||"",n.getAttribute("style")===""&&n.removeAttribute("style")):n.nodeType===3&&(t?(n._stashedText=n.nodeValue,n.nodeValue=""):n.nodeValue=n._stashedText||""),l&&l.nodeType===8)if(n=l.data,n==="/$"){if(e===0)break;e--}else n!=="$"&&n!=="$?"&&n!=="$~"&&n!=="$!"||e++;n=l}while(n)}function cr(e){var t=e.firstChild;for(t&&t.nodeType===10&&(t=t.nextSibling);t;){var n=t;switch(t=t.nextSibling,n.nodeName){case"HTML":case"HEAD":case"BODY":cr(n),vr(n);continue;case"SCRIPT":case"STYLE":continue;case"LINK":if(n.rel.toLowerCase()==="stylesheet")continue}e.removeChild(n)}}function by(e,t,n,l){for(;e.nodeType===1;){var a=n;if(e.nodeName.toLowerCase()!==t.toLowerCase()){if(!l&&(e.nodeName!=="INPUT"||e.type!=="hidden"))break}else if(l){if(!e[Ko])switch(t){case"meta":if(!e.hasAttribute("itemprop"))break;return e;case"link":if(o=e.getAttribute("rel"),o==="stylesheet"&&e.hasAttribute("data-precedence"))break;if(o!==a.rel||e.getAttribute("href")!==(a.href==null||a.href===""?null:a.href)||e.getAttribute("crossorigin")!==(a.crossOrigin==null?null:a.crossOrigin)||e.getAttribute("title")!==(a.title==null?null:a.title))break;return e;case"style":if(e.hasAttribute("data-precedence"))break;return e;case"script":if(o=e.getAttribute("src"),(o!==(a.src==null?null:a.src)||e.getAttribute("type")!==(a.type==null?null:a.type)||e.getAttribute("crossorigin")!==(a.crossOrigin==null?null:a.crossOrigin))&&o&&e.hasAttribute("async")&&!e.hasAttribute("itemprop"))break;return e;default:return e}}else if(t==="input"&&e.type==="hidden"){var o=a.name==null?null:""+a.name;if(a.type==="hidden"&&e.getAttribute("name")===o)return e}else return e;if(e=Ut(e.nextSibling),e===null)break}return null}function vy(e,t,n){if(t==="")return null;for(;e.nodeType!==3;)if((e.nodeType!==1||e.nodeName!=="INPUT"||e.type!=="hidden")&&!n||(e=Ut(e.nextSibling),e===null))return null;return e}function Qm(e,t){for(;e.nodeType!==8;)if((e.nodeType!==1||e.nodeName!=="INPUT"||e.type!=="hidden")&&!t||(e=Ut(e.nextSibling),e===null))return null;return e}function rr(e){return e.data==="$?"||e.data==="$~"}function dr(e){return e.data==="$!"||e.data==="$?"&&e.ownerDocument.readyState!=="loading"}function Sy(e,t){var n=e.ownerDocument;if(e.data==="$~")e._reactRetry=t;else if(e.data!=="$?"||n.readyState!=="loading")t();else{var l=function(){t(),n.removeEventListener("DOMContentLoaded",l)};n.addEventListener("DOMContentLoaded",l),e._reactRetry=l}}function Ut(e){for(;e!=null;e=e.nextSibling){var t=e.nodeType;if(t===1||t===3)break;if(t===8){if(t=e.data,t==="$"||t==="$!"||t==="$?"||t==="$~"||t==="&"||t==="F!"||t==="F")break;if(t==="/$"||t==="/&")return null}}return e}var _r=null;function t1(e){e=e.nextSibling;for(var t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="/$"||n==="/&"){if(t===0)return Ut(e.nextSibling);t--}else n!=="$"&&n!=="$!"&&n!=="$?"&&n!=="$~"&&n!=="&"||t++}e=e.nextSibling}return null}function n1(e){e=e.previousSibling;for(var t=0;e;){if(e.nodeType===8){var n=e.data;if(n==="$"||n==="$!"||n==="$?"||n==="$~"||n==="&"){if(t===0)return e;t--}else n!=="/$"&&n!=="/&"||t++}e=e.previousSibling}return null}function qm(e,t,n){switch(t=ks(n),e){case"html":if(e=t.documentElement,!e)throw Error(E(452));return e;case"head":if(e=t.head,!e)throw Error(E(453));return e;case"body":if(e=t.body,!e)throw Error(E(454));return e;default:throw Error(E(451))}}function Ao(e){for(var t=e.attributes;t.length;)e.removeAttributeNode(t[0]);vr(e)}var jt=new Map,l1=new Set;function Ms(e){return typeof e.getRootNode=="function"?e.getRootNode():e.nodeType===9?e:e.ownerDocument}var On=ce.d;ce.d={f:xy,r:Cy,D:wy,C:Ey,L:Ty,m:ky,X:Ay,S:My,M:zy};function xy(){var e=On.f(),t=Zs();return e||t}function Cy(e){var t=Ha(e);t!==null&&t.tag===5&&t.type==="form"?H0(t):On.r(e)}var ja=typeof document>"u"?null:document;function $m(e,t,n){var l=ja;if(l&&typeof t=="string"&&t){var a=Bt(t);a='link[rel="'+e+'"][href="'+a+'"]',typeof n=="string"&&(a+='[crossorigin="'+n+'"]'),l1.has(a)||(l1.add(a),e={rel:e,crossOrigin:n,href:t},l.querySelector(a)===null&&(t=l.createElement("link"),Pe(t,"link",e),Ve(t),l.head.appendChild(t)))}}function wy(e){On.D(e),$m("dns-prefetch",e,null)}function Ey(e,t){On.C(e,t),$m("preconnect",e,t)}function Ty(e,t,n){On.L(e,t,n);var l=ja;if(l&&e&&t){var a='link[rel="preload"][as="'+Bt(t)+'"]';t==="image"&&n&&n.imageSrcSet?(a+='[imagesrcset="'+Bt(n.imageSrcSet)+'"]',typeof n.imageSizes=="string"&&(a+='[imagesizes="'+Bt(n.imageSizes)+'"]')):a+='[href="'+Bt(e)+'"]';var o=a;switch(t){case"style":o=Oa(e);break;case"script":o=Xa(e)}jt.has(o)||(e=we({rel:"preload",href:t==="image"&&n&&n.imageSrcSet?void 0:e,as:t},n),jt.set(o,e),l.querySelector(a)!==null||t==="style"&&l.querySelector(ei(o))||t==="script"&&l.querySelector(ti(o))||(t=l.createElement("link"),Pe(t,"link",e),Ve(t),l.head.appendChild(t)))}}function ky(e,t){On.m(e,t);var n=ja;if(n&&e){var l=t&&typeof t.as=="string"?t.as:"script",a='link[rel="modulepreload"][as="'+Bt(l)+'"][href="'+Bt(e)+'"]',o=a;switch(l){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":o=Xa(e)}if(!jt.has(o)&&(e=we({rel:"modulepreload",href:e},t),jt.set(o,e),n.querySelector(a)===null)){switch(l){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":if(n.querySelector(ti(o)))return}l=n.createElement("link"),Pe(l,"link",e),Ve(l),n.head.appendChild(l)}}}function My(e,t,n){On.S(e,t,n);var l=ja;if(l&&e){var a=ga(l).hoistableStyles,o=Oa(e);t=t||"default";var i=a.get(o);if(!i){var s={loading:0,preload:null};if(i=l.querySelector(ei(o)))s.loading=5;else{e=we({rel:"stylesheet",href:e,"data-precedence":t},n),(n=jt.get(o))&&od(e,n);var u=i=l.createElement("link");Ve(u),Pe(u,"link",e),u._p=new Promise(function(h,y){u.onload=h,u.onerror=y}),u.addEventListener("load",function(){s.loading|=1}),u.addEventListener("error",function(){s.loading|=2}),s.loading|=4,es(i,t,l)}i={type:"stylesheet",instance:i,count:1,state:s},a.set(o,i)}}}function Ay(e,t){On.X(e,t);var n=ja;if(n&&e){var l=ga(n).hoistableScripts,a=Xa(e),o=l.get(a);o||(o=n.querySelector(ti(a)),o||(e=we({src:e,async:!0},t),(t=jt.get(a))&&id(e,t),o=n.createElement("script"),Ve(o),Pe(o,"link",e),n.head.appendChild(o)),o={type:"script",instance:o,count:1,state:null},l.set(a,o))}}function zy(e,t){On.M(e,t);var n=ja;if(n&&e){var l=ga(n).hoistableScripts,a=Xa(e),o=l.get(a);o||(o=n.querySelector(ti(a)),o||(e=we({src:e,async:!0,type:"module"},t),(t=jt.get(a))&&id(e,t),o=n.createElement("script"),Ve(o),Pe(o,"link",e),n.head.appendChild(o)),o={type:"script",instance:o,count:1,state:null},l.set(a,o))}}function a1(e,t,n,l){var a=(a=In.current)?Ms(a):null;if(!a)throw Error(E(446));switch(e){case"meta":case"title":return null;case"style":return typeof n.precedence=="string"&&typeof n.href=="string"?(t=Oa(n.href),n=ga(a).hoistableStyles,l=n.get(t),l||(l={type:"style",instance:null,count:0,state:null},n.set(t,l)),l):{type:"void",instance:null,count:0,state:null};case"link":if(n.rel==="stylesheet"&&typeof n.href=="string"&&typeof n.precedence=="string"){e=Oa(n.href);var o=ga(a).hoistableStyles,i=o.get(e);if(i||(a=a.ownerDocument||a,i={type:"stylesheet",instance:null,count:0,state:{loading:0,preload:null}},o.set(e,i),(o=a.querySelector(ei(e)))&&!o._p&&(i.instance=o,i.state.loading=5),jt.has(e)||(n={rel:"preload",as:"style",href:n.href,crossOrigin:n.crossOrigin,integrity:n.integrity,media:n.media,hrefLang:n.hrefLang,referrerPolicy:n.referrerPolicy},jt.set(e,n),o||Ny(a,e,n,i.state))),t&&l===null)throw Error(E(528,""));return i}if(t&&l!==null)throw Error(E(529,""));return null;case"script":return t=n.async,n=n.src,typeof n=="string"&&t&&typeof t!="function"&&typeof t!="symbol"?(t=Xa(n),n=ga(a).hoistableScripts,l=n.get(t),l||(l={type:"script",instance:null,count:0,state:null},n.set(t,l)),l):{type:"void",instance:null,count:0,state:null};default:throw Error(E(444,e))}}function Oa(e){return'href="'+Bt(e)+'"'}function ei(e){return'link[rel="stylesheet"]['+e+"]"}function Zm(e){return we({},e,{"data-precedence":e.precedence,precedence:null})}function Ny(e,t,n,l){e.querySelector('link[rel="preload"][as="style"]['+t+"]")?l.loading=1:(t=e.createElement("link"),l.preload=t,t.addEventListener("load",function(){return l.loading|=1}),t.addEventListener("error",function(){return l.loading|=2}),Pe(t,"link",n),Ve(t),e.head.appendChild(t))}function Xa(e){return'[src="'+Bt(e)+'"]'}function ti(e){return"script[async]"+e}function o1(e,t,n){if(t.count++,t.instance===null)switch(t.type){case"style":var l=e.querySelector('style[data-href~="'+Bt(n.href)+'"]');if(l)return t.instance=l,Ve(l),l;var a=we({},n,{"data-href":n.href,"data-precedence":n.precedence,href:null,precedence:null});return l=(e.ownerDocument||e).createElement("style"),Ve(l),Pe(l,"style",a),es(l,n.precedence,e),t.instance=l;case"stylesheet":a=Oa(n.href);var o=e.querySelector(ei(a));if(o)return t.state.loading|=4,t.instance=o,Ve(o),o;l=Zm(n),(a=jt.get(a))&&od(l,a),o=(e.ownerDocument||e).createElement("link"),Ve(o);var i=o;return i._p=new Promise(function(s,u){i.onload=s,i.onerror=u}),Pe(o,"link",l),t.state.loading|=4,es(o,n.precedence,e),t.instance=o;case"script":return o=Xa(n.src),(a=e.querySelector(ti(o)))?(t.instance=a,Ve(a),a):(l=n,(a=jt.get(o))&&(l=we({},n),id(l,a)),e=e.ownerDocument||e,a=e.createElement("script"),Ve(a),Pe(a,"link",l),e.head.appendChild(a),t.instance=a);case"void":return null;default:throw Error(E(443,t.type))}else t.type==="stylesheet"&&(t.state.loading&4)===0&&(l=t.instance,t.state.loading|=4,es(l,n.precedence,e));return t.instance}function es(e,t,n){for(var l=n.querySelectorAll('link[rel="stylesheet"][data-precedence],style[data-precedence]'),a=l.length?l[l.length-1]:null,o=a,i=0;i<l.length;i++){var s=l[i];if(s.dataset.precedence===t)o=s;else if(o!==a)break}o?o.parentNode.insertBefore(e,o.nextSibling):(t=n.nodeType===9?n.head:n,t.insertBefore(e,t.firstChild))}function od(e,t){e.crossOrigin==null&&(e.crossOrigin=t.crossOrigin),e.referrerPolicy==null&&(e.referrerPolicy=t.referrerPolicy),e.title==null&&(e.title=t.title)}function id(e,t){e.crossOrigin==null&&(e.crossOrigin=t.crossOrigin),e.referrerPolicy==null&&(e.referrerPolicy=t.referrerPolicy),e.integrity==null&&(e.integrity=t.integrity)}var ts=null;function i1(e,t,n){if(ts===null){var l=new Map,a=ts=new Map;a.set(n,l)}else a=ts,l=a.get(n),l||(l=new Map,a.set(n,l));if(l.has(e))return l;for(l.set(e,null),n=n.getElementsByTagName(e),a=0;a<n.length;a++){var o=n[a];if(!(o[Ko]||o[We]||e==="link"&&o.getAttribute("rel")==="stylesheet")&&o.namespaceURI!=="http://www.w3.org/2000/svg"){var i=o.getAttribute(t)||"";i=e+i;var s=l.get(i);s?s.push(o):l.set(i,[o])}}return l}function s1(e,t,n){e=e.ownerDocument||e,e.head.insertBefore(n,t==="title"?e.querySelector("head > title"):null)}function Ly(e,t,n){if(n===1||t.itemProp!=null)return!1;switch(e){case"meta":case"title":return!0;case"style":if(typeof t.precedence!="string"||typeof t.href!="string"||t.href==="")break;return!0;case"link":if(typeof t.rel!="string"||typeof t.href!="string"||t.href===""||t.onLoad||t.onError)break;return t.rel==="stylesheet"?(e=t.disabled,typeof t.precedence=="string"&&e==null):!0;case"script":if(t.async&&typeof t.async!="function"&&typeof t.async!="symbol"&&!t.onLoad&&!t.onError&&t.src&&typeof t.src=="string")return!0}return!1}function Gm(e){return!(e.type==="stylesheet"&&(e.state.loading&3)===0)}function Oy(e,t,n,l){if(n.type==="stylesheet"&&(typeof l.media!="string"||matchMedia(l.media).matches!==!1)&&(n.state.loading&4)===0){if(n.instance===null){var a=Oa(l.href),o=t.querySelector(ei(a));if(o){t=o._p,t!==null&&typeof t=="object"&&typeof t.then=="function"&&(e.count++,e=As.bind(e),t.then(e,e)),n.state.loading|=4,n.instance=o,Ve(o);return}o=t.ownerDocument||t,l=Zm(l),(a=jt.get(a))&&od(l,a),o=o.createElement("link"),Ve(o);var i=o;i._p=new Promise(function(s,u){i.onload=s,i.onerror=u}),Pe(o,"link",l),n.instance=o}e.stylesheets===null&&(e.stylesheets=new Map),e.stylesheets.set(n,t),(t=n.state.preload)&&(n.state.loading&3)===0&&(e.count++,n=As.bind(e),t.addEventListener("load",n),t.addEventListener("error",n))}}var bc=0;function Dy(e,t){return e.stylesheets&&e.count===0&&ns(e,e.stylesheets),0<e.count||0<e.imgCount?function(n){var l=setTimeout(function(){if(e.stylesheets&&ns(e,e.stylesheets),e.unsuspend){var o=e.unsuspend;e.unsuspend=null,o()}},6e4+t);0<e.imgBytes&&bc===0&&(bc=62500*my());var a=setTimeout(function(){if(e.waitingForImages=!1,e.count===0&&(e.stylesheets&&ns(e,e.stylesheets),e.unsuspend)){var o=e.unsuspend;e.unsuspend=null,o()}},(e.imgBytes>bc?50:800)+t);return e.unsuspend=n,function(){e.unsuspend=null,clearTimeout(l),clearTimeout(a)}}:null}function As(){if(this.count--,this.count===0&&(this.imgCount===0||!this.waitingForImages)){if(this.stylesheets)ns(this,this.stylesheets);else if(this.unsuspend){var e=this.unsuspend;this.unsuspend=null,e()}}}var zs=null;function ns(e,t){e.stylesheets=null,e.unsuspend!==null&&(e.count++,zs=new Map,t.forEach(By,e),zs=null,As.call(e))}function By(e,t){if(!(t.state.loading&4)){var n=zs.get(e);if(n)var l=n.get(null);else{n=new Map,zs.set(e,n);for(var a=e.querySelectorAll("link[data-precedence],style[data-precedence]"),o=0;o<a.length;o++){var i=a[o];(i.nodeName==="LINK"||i.getAttribute("media")!=="not all")&&(n.set(i.dataset.precedence,i),l=i)}l&&n.set(null,l)}a=t.instance,i=a.getAttribute("data-precedence"),o=n.get(i)||l,o===l&&n.set(null,a),n.set(i,a),this.count++,l=As.bind(this),a.addEventListener("load",l),a.addEventListener("error",l),o?o.parentNode.insertBefore(a,o.nextSibling):(e=e.nodeType===9?e.head:e,e.insertBefore(a,e.firstChild)),t.state.loading|=4}}var Xo={$$typeof:xn,Provider:null,Consumer:null,_currentValue:El,_currentValue2:El,_threadCount:0};function Hy(e,t,n,l,a,o,i,s,u){this.tag=1,this.containerInfo=e,this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.next=this.pendingContext=this.context=this.cancelPendingCommit=null,this.callbackPriority=0,this.expirationTimes=Zu(-1),this.entangledLanes=this.shellSuspendCounter=this.errorRecoveryDisabledLanes=this.expiredLanes=this.warmLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Zu(0),this.hiddenUpdates=Zu(null),this.identifierPrefix=l,this.onUncaughtError=a,this.onCaughtError=o,this.onRecoverableError=i,this.pooledCache=null,this.pooledCacheLanes=0,this.formState=u,this.incompleteTransitions=new Map}function Vm(e,t,n,l,a,o,i,s,u,h,y,S){return e=new Hy(e,t,n,i,u,h,y,S,s),t=1,o===!0&&(t|=24),o=xt(3,null,null,t),e.current=o,o.stateNode=e,t=Lr(),t.refCount++,e.pooledCache=t,t.refCount++,o.memoizedState={element:l,isDehydrated:n,cache:t},Br(o),e}function Km(e){return e?(e=fa,e):fa}function Jm(e,t,n,l,a,o){a=Km(a),l.context===null?l.context=a:l.pendingContext=a,l=Pn(t),l.payload={element:n},o=o===void 0?null:o,o!==null&&(l.callback=o),n=el(e,l,t),n!==null&&(ft(n,e,t),So(n,e,t))}function u1(e,t){if(e=e.memoizedState,e!==null&&e.dehydrated!==null){var n=e.retryLane;e.retryLane=n!==0&&n<t?n:t}}function sd(e,t){u1(e,t),(e=e.alternate)&&u1(e,t)}function Wm(e){if(e.tag===13||e.tag===31){var t=Rl(e,67108864);t!==null&&ft(t,e,67108864),sd(e,67108864)}}function c1(e){if(e.tag===13||e.tag===31){var t=kt();t=pr(t);var n=Rl(e,t);n!==null&&ft(n,e,t),sd(e,t)}}var Ns=!0;function Yy(e,t,n,l){var a=j.T;j.T=null;var o=ce.p;try{ce.p=2,ud(e,t,n,l)}finally{ce.p=o,j.T=a}}function Ry(e,t,n,l){var a=j.T;j.T=null;var o=ce.p;try{ce.p=8,ud(e,t,n,l)}finally{ce.p=o,j.T=a}}function ud(e,t,n,l){if(Ns){var a=fr(l);if(a===null)gc(e,t,l,Ls,n),r1(e,l);else if(jy(a,e,t,n,l))l.stopPropagation();else if(r1(e,l),t&4&&-1<Uy.indexOf(e)){for(;a!==null;){var o=Ha(a);if(o!==null)switch(o.tag){case 3:if(o=o.stateNode,o.current.memoizedState.isDehydrated){var i=xl(o.pendingLanes);if(i!==0){var s=o;for(s.pendingLanes|=2,s.entangledLanes|=2;i;){var u=1<<31-Tt(i);s.entanglements[1]|=u,i&=~u}ln(o),(ue&6)===0&&(Ss=wt()+500,Po(0,!1))}}break;case 31:case 13:s=Rl(o,2),s!==null&&ft(s,o,2),Zs(),sd(o,2)}if(o=fr(l),o===null&&gc(e,t,l,Ls,n),o===a)break;a=o}a!==null&&l.stopPropagation()}else gc(e,t,l,null,n)}}function fr(e){return e=xr(e),cd(e)}var Ls=null;function cd(e){if(Ls=null,e=sa(e),e!==null){var t=$o(e);if(t===null)e=null;else{var n=t.tag;if(n===13){if(e=y1(t),e!==null)return e;e=null}else if(n===31){if(e=g1(t),e!==null)return e;e=null}else if(n===3){if(t.stateNode.current.memoizedState.isDehydrated)return t.tag===3?t.stateNode.containerInfo:null;e=null}else t!==e&&(e=null)}}return Ls=e,null}function Im(e){switch(e){case"beforetoggle":case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"toggle":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 2;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 8;case"message":switch(T2()){case S1:return 2;case x1:return 8;case ss:case k2:return 32;case C1:return 268435456;default:return 32}default:return 32}}var mr=!1,ll=null,al=null,ol=null,Qo=new Map,qo=new Map,Zn=[],Uy="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(" ");function r1(e,t){switch(e){case"focusin":case"focusout":ll=null;break;case"dragenter":case"dragleave":al=null;break;case"mouseover":case"mouseout":ol=null;break;case"pointerover":case"pointerout":Qo.delete(t.pointerId);break;case"gotpointercapture":case"lostpointercapture":qo.delete(t.pointerId)}}function co(e,t,n,l,a,o){return e===null||e.nativeEvent!==o?(e={blockedOn:t,domEventName:n,eventSystemFlags:l,nativeEvent:o,targetContainers:[a]},t!==null&&(t=Ha(t),t!==null&&Wm(t)),e):(e.eventSystemFlags|=l,t=e.targetContainers,a!==null&&t.indexOf(a)===-1&&t.push(a),e)}function jy(e,t,n,l,a){switch(t){case"focusin":return ll=co(ll,e,t,n,l,a),!0;case"dragenter":return al=co(al,e,t,n,l,a),!0;case"mouseover":return ol=co(ol,e,t,n,l,a),!0;case"pointerover":var o=a.pointerId;return Qo.set(o,co(Qo.get(o)||null,e,t,n,l,a)),!0;case"gotpointercapture":return o=a.pointerId,qo.set(o,co(qo.get(o)||null,e,t,n,l,a)),!0}return!1}function Fm(e){var t=sa(e.target);if(t!==null){var n=$o(t);if(n!==null){if(t=n.tag,t===13){if(t=y1(n),t!==null){e.blockedOn=t,G_(e.priority,function(){c1(n)});return}}else if(t===31){if(t=g1(n),t!==null){e.blockedOn=t,G_(e.priority,function(){c1(n)});return}}else if(t===3&&n.stateNode.current.memoizedState.isDehydrated){e.blockedOn=n.tag===3?n.stateNode.containerInfo:null;return}}}e.blockedOn=null}function ls(e){if(e.blockedOn!==null)return!1;for(var t=e.targetContainers;0<t.length;){var n=fr(e.nativeEvent);if(n===null){n=e.nativeEvent;var l=new n.constructor(n.type,n);Lc=l,n.target.dispatchEvent(l),Lc=null}else return t=Ha(n),t!==null&&Wm(t),e.blockedOn=n,!1;t.shift()}return!0}function d1(e,t,n){ls(e)&&n.delete(t)}function Xy(){mr=!1,ll!==null&&ls(ll)&&(ll=null),al!==null&&ls(al)&&(al=null),ol!==null&&ls(ol)&&(ol=null),Qo.forEach(d1),qo.forEach(d1)}function Xi(e,t){e.blockedOn===t&&(e.blockedOn=null,mr||(mr=!0,$e.unstable_scheduleCallback($e.unstable_NormalPriority,Xy)))}var Qi=null;function _1(e){Qi!==e&&(Qi=e,$e.unstable_scheduleCallback($e.unstable_NormalPriority,function(){Qi===e&&(Qi=null);for(var t=0;t<e.length;t+=3){var n=e[t],l=e[t+1],a=e[t+2];if(typeof l!="function"){if(cd(l||n)===null)continue;break}var o=Ha(n);o!==null&&(e.splice(t,3),t-=3,Kc(o,{pending:!0,data:a,method:n.method,action:l},l,a))}}))}function Da(e){function t(u){return Xi(u,e)}ll!==null&&Xi(ll,e),al!==null&&Xi(al,e),ol!==null&&Xi(ol,e),Qo.forEach(t),qo.forEach(t);for(var n=0;n<Zn.length;n++){var l=Zn[n];l.blockedOn===e&&(l.blockedOn=null)}for(;0<Zn.length&&(n=Zn[0],n.blockedOn===null);)Fm(n),n.blockedOn===null&&Zn.shift();if(n=(e.ownerDocument||e).$$reactFormReplay,n!=null)for(l=0;l<n.length;l+=3){var a=n[l],o=n[l+1],i=a[mt]||null;if(typeof o=="function")i||_1(n);else if(i){var s=null;if(o&&o.hasAttribute("formAction")){if(a=o,i=o[mt]||null)s=i.formAction;else if(cd(a)!==null)continue}else s=i.action;typeof s=="function"?n[l+1]=s:(n.splice(l,3),l-=3),_1(n)}}}function Pm(){function e(o){o.canIntercept&&o.info==="react-transition"&&o.intercept({handler:function(){return new Promise(function(i){return a=i})},focusReset:"manual",scroll:"manual"})}function t(){a!==null&&(a(),a=null),l||setTimeout(n,20)}function n(){if(!l&&!navigation.transition){var o=navigation.currentEntry;o&&o.url!=null&&navigation.navigate(o.url,{state:o.getState(),info:"react-transition",history:"replace"})}}if(typeof navigation=="object"){var l=!1,a=null;return navigation.addEventListener("navigate",e),navigation.addEventListener("navigatesuccess",t),navigation.addEventListener("navigateerror",t),setTimeout(n,100),function(){l=!0,navigation.removeEventListener("navigate",e),navigation.removeEventListener("navigatesuccess",t),navigation.removeEventListener("navigateerror",t),a!==null&&(a(),a=null)}}}function rd(e){this._internalRoot=e}Ks.prototype.render=rd.prototype.render=function(e){var t=this._internalRoot;if(t===null)throw Error(E(409));var n=t.current,l=kt();Jm(n,l,e,t,null,null)};Ks.prototype.unmount=rd.prototype.unmount=function(){var e=this._internalRoot;if(e!==null){this._internalRoot=null;var t=e.containerInfo;Jm(e.current,2,null,e,null,null),Zs(),t[Ba]=null}};function Ks(e){this._internalRoot=e}Ks.prototype.unstable_scheduleHydration=function(e){if(e){var t=M1();e={blockedOn:null,target:e,priority:t};for(var n=0;n<Zn.length&&t!==0&&t<Zn[n].priority;n++);Zn.splice(n,0,e),n===0&&Fm(e)}};var f1=m1.version;if(f1!=="19.2.4")throw Error(E(527,f1,"19.2.4"));ce.findDOMNode=function(e){var t=e._reactInternals;if(t===void 0)throw typeof e.render=="function"?Error(E(188)):(e=Object.keys(e).join(","),Error(E(268,e)));return e=b2(t),e=e!==null?p1(e):null,e=e===null?null:e.stateNode,e};var Qy={bundleType:0,version:"19.2.4",rendererPackageName:"react-dom",currentDispatcherRef:j,reconcilerVersion:"19.2.4"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"&&(ro=__REACT_DEVTOOLS_GLOBAL_HOOK__,!ro.isDisabled&&ro.supportsFiber))try{Zo=ro.inject(Qy),Et=ro}catch{}var ro;Js.createRoot=function(e,t){if(!h1(e))throw Error(E(299));var n=!1,l="",a=$0,o=Z0,i=G0;return t!=null&&(t.unstable_strictMode===!0&&(n=!0),t.identifierPrefix!==void 0&&(l=t.identifierPrefix),t.onUncaughtError!==void 0&&(a=t.onUncaughtError),t.onCaughtError!==void 0&&(o=t.onCaughtError),t.onRecoverableError!==void 0&&(i=t.onRecoverableError)),t=Vm(e,1,!1,null,null,n,l,null,a,o,i,Pm),e[Ba]=t.current,ad(e),new rd(t)};Js.hydrateRoot=function(e,t,n){if(!h1(e))throw Error(E(299));var l=!1,a="",o=$0,i=Z0,s=G0,u=null;return n!=null&&(n.unstable_strictMode===!0&&(l=!0),n.identifierPrefix!==void 0&&(a=n.identifierPrefix),n.onUncaughtError!==void 0&&(o=n.onUncaughtError),n.onCaughtError!==void 0&&(i=n.onCaughtError),n.onRecoverableError!==void 0&&(s=n.onRecoverableError),n.formState!==void 0&&(u=n.formState)),t=Vm(e,1,!0,t,n??null,l,a,u,o,i,s,Pm),t.context=Km(null),n=t.current,l=kt(),l=pr(l),a=Pn(l),a.callback=null,el(n,a,l),n=l,t.current.lanes=n,Vo(t,n),ln(t),e[Ba]=t.current,ad(e),new Ks(t)};Js.version="19.2.4"});var l5=Wt((rp,n5)=>{"use strict";function t5(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(t5)}catch(e){console.error(e)}}t5(),n5.exports=e5()});var o5=Wt(Ws=>{"use strict";var qy=Symbol.for("react.transitional.element"),$y=Symbol.for("react.fragment");function a5(e,t,n){var l=null;if(n!==void 0&&(l=""+n),t.key!==void 0&&(l=""+t.key),"key"in t){n={};for(var a in t)a!=="key"&&(n[a]=t[a])}else n=t;return t=n.ref,{$$typeof:qy,type:e,key:l,ref:t!==void 0?t:null,props:n}}Ws.Fragment=$y;Ws.jsx=a5;Ws.jsxs=a5});var Is=Wt((_p,i5)=>{"use strict";i5.exports=o5()});var Dn=fn(bl()),k5=fn(l5());var w=fn(bl(),1),Sd=fn(ju(),1),Ae=fn(bl(),1),M=fn(Is(),1),ke=fn(Is(),1),C5=fn(bl(),1),m=fn(Is(),1),Zy=`.styles-module__popup___IhzrD svg[fill=none] {
  fill: none !important;
}
.styles-module__popup___IhzrD svg[fill=none] :not([fill]) {
  fill: none !important;
}

@keyframes styles-module__popupEnter___AuQDN {
  from {
    opacity: 0;
    transform: translateX(-50%) scale(0.95) translateY(4px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) scale(1) translateY(0);
  }
}
@keyframes styles-module__popupExit___JJKQX {
  from {
    opacity: 1;
    transform: translateX(-50%) scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: translateX(-50%) scale(0.95) translateY(4px);
  }
}
@keyframes styles-module__shake___jdbWe {
  0%, 100% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(0);
  }
  20% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(-3px);
  }
  40% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(3px);
  }
  60% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(-2px);
  }
  80% {
    transform: translateX(-50%) scale(1) translateY(0) translateX(2px);
  }
}
.styles-module__popup___IhzrD {
  position: fixed;
  transform: translateX(-50%);
  width: 280px;
  padding: 0.75rem 1rem 14px;
  background: #1a1a1a;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
  cursor: default;
  z-index: 100001;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  will-change: transform, opacity;
  opacity: 0;
}
.styles-module__popup___IhzrD.styles-module__enter___L7U7N {
  animation: styles-module__popupEnter___AuQDN 0.2s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}
.styles-module__popup___IhzrD.styles-module__entered___COX-w {
  opacity: 1;
  transform: translateX(-50%) scale(1) translateY(0);
}
.styles-module__popup___IhzrD.styles-module__exit___5eGjE {
  animation: styles-module__popupExit___JJKQX 0.15s ease-in forwards;
}
.styles-module__popup___IhzrD.styles-module__entered___COX-w.styles-module__shake___jdbWe {
  animation: styles-module__shake___jdbWe 0.25s ease-out;
}

.styles-module__header___wWsSi {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5625rem;
}

.styles-module__element___fTV2z {
  font-size: 0.75rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}

.styles-module__headerToggle___WpW0b {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  flex: 1;
  min-width: 0;
  text-align: left;
}
.styles-module__headerToggle___WpW0b .styles-module__element___fTV2z {
  flex: 1;
}

.styles-module__chevron___ZZJlR {
  color: rgba(255, 255, 255, 0.5);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  flex-shrink: 0;
}
.styles-module__chevron___ZZJlR.styles-module__expanded___2Hxgv {
  transform: rotate(90deg);
}

.styles-module__stylesWrapper___pnHgy {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.styles-module__stylesWrapper___pnHgy.styles-module__expanded___2Hxgv {
  grid-template-rows: 1fr;
}

.styles-module__stylesInner___YYZe2 {
  overflow: hidden;
}

.styles-module__stylesBlock___VfQKn {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.375rem;
  padding: 0.5rem 0.625rem;
  margin-bottom: 0.5rem;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.6875rem;
  line-height: 1.5;
}

.styles-module__styleLine___1YQiD {
  color: rgba(255, 255, 255, 0.85);
  word-break: break-word;
}

.styles-module__styleProperty___84L1i {
  color: #c792ea;
}

.styles-module__styleValue___q51-h {
  color: rgba(255, 255, 255, 0.85);
}

.styles-module__timestamp___Dtpsv {
  font-size: 0.625rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.35);
  font-variant-numeric: tabular-nums;
  margin-left: 0.5rem;
  flex-shrink: 0;
}

.styles-module__quote___mcMmQ {
  font-size: 12px;
  font-style: italic;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.5rem;
  padding: 0.4rem 0.5rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 0.25rem;
  line-height: 1.45;
}

.styles-module__textarea___jrSae {
  width: 100%;
  padding: 0.5rem 0.625rem;
  font-size: 0.8125rem;
  font-family: inherit;
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  resize: none;
  outline: none;
  transition: border-color 0.15s ease;
}
.styles-module__textarea___jrSae:focus {
  border-color: #3c82f7;
}
.styles-module__textarea___jrSae.styles-module__green___99l3h:focus {
  border-color: #34c759;
}
.styles-module__textarea___jrSae::placeholder {
  color: rgba(255, 255, 255, 0.35);
}
.styles-module__textarea___jrSae::-webkit-scrollbar {
  width: 6px;
}
.styles-module__textarea___jrSae::-webkit-scrollbar-track {
  background: transparent;
}
.styles-module__textarea___jrSae::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.styles-module__actions___D6x3f {
  display: flex;
  justify-content: flex-end;
  gap: 0.375rem;
  margin-top: 0.5rem;
}

.styles-module__cancel___hRjnL,
.styles-module__submit___K-mIR {
  padding: 0.4rem 0.875rem;
  font-size: 0.75rem;
  font-weight: 500;
  border-radius: 1rem;
  border: none;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease, opacity 0.15s ease;
}

.styles-module__cancel___hRjnL {
  background: transparent;
  color: rgba(255, 255, 255, 0.5);
}
.styles-module__cancel___hRjnL:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.styles-module__submit___K-mIR {
  color: white;
}
.styles-module__submit___K-mIR:hover:not(:disabled) {
  filter: brightness(0.9);
}
.styles-module__submit___K-mIR:disabled {
  cursor: not-allowed;
}

.styles-module__deleteWrapper___oSjdo {
  margin-right: auto;
}

.styles-module__deleteButton___4VuAE {
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.4);
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
}
.styles-module__deleteButton___4VuAE:hover {
  background: rgba(255, 59, 48, 0.25);
  color: #ff3b30;
}
.styles-module__deleteButton___4VuAE:active {
  transform: scale(0.92);
}

.styles-module__light___6AaSQ.styles-module__popup___IhzrD {
  background: #fff;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.06);
}
.styles-module__light___6AaSQ .styles-module__element___fTV2z {
  color: rgba(0, 0, 0, 0.6);
}
.styles-module__light___6AaSQ .styles-module__timestamp___Dtpsv {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__chevron___ZZJlR {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__stylesBlock___VfQKn {
  background: rgba(0, 0, 0, 0.03);
}
.styles-module__light___6AaSQ .styles-module__styleLine___1YQiD {
  color: rgba(0, 0, 0, 0.75);
}
.styles-module__light___6AaSQ .styles-module__styleProperty___84L1i {
  color: #7c3aed;
}
.styles-module__light___6AaSQ .styles-module__styleValue___q51-h {
  color: rgba(0, 0, 0, 0.75);
}
.styles-module__light___6AaSQ .styles-module__quote___mcMmQ {
  color: rgba(0, 0, 0, 0.55);
  background: rgba(0, 0, 0, 0.04);
}
.styles-module__light___6AaSQ .styles-module__textarea___jrSae {
  background: rgba(0, 0, 0, 0.03);
  color: #1a1a1a;
  border-color: rgba(0, 0, 0, 0.12);
}
.styles-module__light___6AaSQ .styles-module__textarea___jrSae::placeholder {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__textarea___jrSae::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.15);
}
.styles-module__light___6AaSQ .styles-module__cancel___hRjnL {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___6AaSQ .styles-module__cancel___hRjnL:hover {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.75);
}
.styles-module__light___6AaSQ .styles-module__deleteButton___4VuAE {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___6AaSQ .styles-module__deleteButton___4VuAE:hover {
  background: rgba(255, 59, 48, 0.15);
  color: #ff3b30;
}`,Gy={popup:"styles-module__popup___IhzrD",enter:"styles-module__enter___L7U7N",popupEnter:"styles-module__popupEnter___AuQDN",entered:"styles-module__entered___COX-w",exit:"styles-module__exit___5eGjE",popupExit:"styles-module__popupExit___JJKQX",shake:"styles-module__shake___jdbWe",header:"styles-module__header___wWsSi",element:"styles-module__element___fTV2z",headerToggle:"styles-module__headerToggle___WpW0b",chevron:"styles-module__chevron___ZZJlR",expanded:"styles-module__expanded___2Hxgv",stylesWrapper:"styles-module__stylesWrapper___pnHgy",stylesInner:"styles-module__stylesInner___YYZe2",stylesBlock:"styles-module__stylesBlock___VfQKn",styleLine:"styles-module__styleLine___1YQiD",styleProperty:"styles-module__styleProperty___84L1i",styleValue:"styles-module__styleValue___q51-h",timestamp:"styles-module__timestamp___Dtpsv",quote:"styles-module__quote___mcMmQ",textarea:"styles-module__textarea___jrSae",green:"styles-module__green___99l3h",actions:"styles-module__actions___D6x3f",cancel:"styles-module__cancel___hRjnL",submit:"styles-module__submit___K-mIR",deleteWrapper:"styles-module__deleteWrapper___oSjdo",deleteButton:"styles-module__deleteButton___4VuAE",light:"styles-module__light___6AaSQ"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-annotation-popup-css-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-annotation-popup-css-styles",e.textContent=Zy,document.head.appendChild(e))}var pe=Gy,Vy=`.icon-transitions-module__iconState___uqK9J {
  transition: opacity 0.2s ease, transform 0.2s ease;
  transform-origin: center;
}

.icon-transitions-module__iconStateFast___HxlMm {
  transition: opacity 0.15s ease, transform 0.15s ease;
  transform-origin: center;
}

.icon-transitions-module__iconFade___nPwXg {
  transition: opacity 0.2s ease;
}

.icon-transitions-module__iconFadeFast___Ofb2t {
  transition: opacity 0.15s ease;
}

.icon-transitions-module__visible___PlHsU {
  opacity: 1 !important;
}

.icon-transitions-module__visibleScaled___8Qog- {
  opacity: 1 !important;
  transform: scale(1);
}

.icon-transitions-module__hidden___ETykt {
  opacity: 0 !important;
}

.icon-transitions-module__hiddenScaled___JXn-m {
  opacity: 0 !important;
  transform: scale(0.8);
}

.icon-transitions-module__sending___uaLN- {
  opacity: 0.5 !important;
  transform: scale(0.8);
}`,Ky={iconState:"icon-transitions-module__iconState___uqK9J",iconStateFast:"icon-transitions-module__iconStateFast___HxlMm",iconFade:"icon-transitions-module__iconFade___nPwXg",iconFadeFast:"icon-transitions-module__iconFadeFast___Ofb2t",visible:"icon-transitions-module__visible___PlHsU",visibleScaled:"icon-transitions-module__visibleScaled___8Qog-",hidden:"icon-transitions-module__hidden___ETykt",hiddenScaled:"icon-transitions-module__hiddenScaled___JXn-m",sending:"icon-transitions-module__sending___uaLN-"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-components-icon-transitions");e||(e=document.createElement("style"),e.id="feedback-tool-styles-components-icon-transitions",e.textContent=Vy,document.head.appendChild(e))}var he=Ky,Jy=({size:e=16})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 16 16",fill:"none",children:(0,M.jsx)("path",{d:"M4 4l8 8M12 4l-8 8",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})}),Wy=({size:e=16})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 16 16",fill:"none",children:(0,M.jsx)("path",{d:"M8 3v10M3 8h10",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})});var Iy=({size:e=24,style:t={}})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",style:t,children:[(0,M.jsxs)("g",{clipPath:"url(#clip0_list_sparkle)",children:[(0,M.jsx)("path",{d:"M11.5 12L5.5 12",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M18.5 6.75L5.5 6.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M9.25 17.25L5.5 17.25",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M16 12.75L16.5179 13.9677C16.8078 14.6494 17.3506 15.1922 18.0323 15.4821L19.25 16L18.0323 16.5179C17.3506 16.8078 16.8078 17.3506 16.5179 18.0323L16 19.25L15.4821 18.0323C15.1922 17.3506 14.6494 16.8078 13.9677 16.5179L12.75 16L13.9677 15.4821C14.6494 15.1922 15.1922 14.6494 15.4821 13.9677L16 12.75Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinejoin:"round"})]}),(0,M.jsx)("defs",{children:(0,M.jsx)("clipPath",{id:"clip0_list_sparkle",children:(0,M.jsx)("rect",{width:"24",height:"24",fill:"white"})})})]}),Qa=({size:e=20})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 20 20",fill:"none",children:[(0,M.jsx)("circle",{cx:"10",cy:"10.5",r:"5.25",stroke:"currentColor",strokeWidth:"1.25"}),(0,M.jsx)("path",{d:"M8.5 8.75C8.5 7.92 9.17 7.25 10 7.25C10.83 7.25 11.5 7.92 11.5 8.75C11.5 9.58 10.83 10.25 10 10.25V11",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("circle",{cx:"10",cy:"13",r:"0.75",fill:"currentColor"})]}),s5=({size:e=14})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 14 14",fill:"none",children:[(0,M.jsx)("style",{children:`
      @keyframes checkDraw {
        0% {
          stroke-dashoffset: 12;
        }
        100% {
          stroke-dashoffset: 0;
        }
      }
      @keyframes checkBounce {
        0% {
          transform: scale(0.5);
          opacity: 0;
        }
        50% {
          transform: scale(1.12);
          opacity: 1;
        }
        75% {
          transform: scale(0.95);
        }
        100% {
          transform: scale(1);
        }
      }
      .check-path-animated {
        stroke-dasharray: 12;
        stroke-dashoffset: 0;
        transform-origin: center;
        animation: checkDraw 0.18s ease-out, checkBounce 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      }
    `}),(0,M.jsx)("path",{className:"check-path-animated",d:"M3.9375 7L6.125 9.1875L10.5 4.8125",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]});var Fy=({size:e=24,copied:t=!1})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,M.jsxs)("g",{className:`${he.iconState} ${t?he.hiddenScaled:he.visibleScaled}`,children:[(0,M.jsx)("path",{d:"M4.75 11.25C4.75 10.4216 5.42157 9.75 6.25 9.75H12.75C13.5784 9.75 14.25 10.4216 14.25 11.25V17.75C14.25 18.5784 13.5784 19.25 12.75 19.25H6.25C5.42157 19.25 4.75 18.5784 4.75 17.75V11.25Z",stroke:"currentColor",strokeWidth:"1.5"}),(0,M.jsx)("path",{d:"M17.25 14.25H17.75C18.5784 14.25 19.25 13.5784 19.25 12.75V6.25C19.25 5.42157 18.5784 4.75 17.75 4.75H11.25C10.4216 4.75 9.75 5.42157 9.75 6.25V6.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})]}),(0,M.jsxs)("g",{className:`${he.iconState} ${t?he.visibleScaled:he.hiddenScaled}`,children:[(0,M.jsx)("path",{d:"M12 20C7.58172 20 4 16.4182 4 12C4 7.58172 7.58172 4 12 4C16.4182 4 20 7.58172 20 12C20 16.4182 16.4182 20 12 20Z",stroke:"#22c55e",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M15 10L11 14.25L9.25 12.25",stroke:"#22c55e",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]})]}),Py=({size:e=24,state:t="idle"})=>{let n=t==="idle",l=t==="sent",a=t==="failed",o=t==="sending";return(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,M.jsx)("g",{className:`${he.iconStateFast} ${n?he.visibleScaled:o?he.sending:he.hiddenScaled}`,children:(0,M.jsx)("path",{d:"M9.875 14.125L12.3506 19.6951C12.7184 20.5227 13.9091 20.4741 14.2083 19.6193L18.8139 6.46032C19.0907 5.6695 18.3305 4.90933 17.5397 5.18611L4.38072 9.79174C3.52589 10.0909 3.47731 11.2816 4.30494 11.6494L9.875 14.125ZM9.875 14.125L13.375 10.625",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})}),(0,M.jsxs)("g",{className:`${he.iconStateFast} ${l?he.visibleScaled:he.hiddenScaled}`,children:[(0,M.jsx)("path",{d:"M12 20C7.58172 20 4 16.4182 4 12C4 7.58172 7.58172 4 12 4C16.4182 4 20 7.58172 20 12C20 16.4182 16.4182 20 12 20Z",stroke:"#22c55e",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M15 10L11 14.25L9.25 12.25",stroke:"#22c55e",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]}),(0,M.jsxs)("g",{className:`${he.iconStateFast} ${a?he.visibleScaled:he.hiddenScaled}`,children:[(0,M.jsx)("path",{d:"M12 20C7.58172 20 4 16.4182 4 12C4 7.58172 7.58172 4 12 4C16.4182 4 20 7.58172 20 12C20 16.4182 16.4182 20 12 20Z",stroke:"#ef4444",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M12 8V12",stroke:"#ef4444",strokeWidth:"1.5",strokeLinecap:"round"}),(0,M.jsx)("circle",{cx:"12",cy:"15",r:"0.5",fill:"#ef4444",stroke:"#ef4444",strokeWidth:"1"})]})]})};var eg=({size:e=24,isOpen:t=!0})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,M.jsxs)("g",{className:`${he.iconFade} ${t?he.visible:he.hidden}`,children:[(0,M.jsx)("path",{d:"M3.91752 12.7539C3.65127 12.2996 3.65037 11.7515 3.9149 11.2962C4.9042 9.59346 7.72688 5.49994 12 5.49994C16.2731 5.49994 19.0958 9.59346 20.0851 11.2962C20.3496 11.7515 20.3487 12.2996 20.0825 12.7539C19.0908 14.4459 16.2694 18.4999 12 18.4999C7.73064 18.4999 4.90918 14.4459 3.91752 12.7539Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M12 14.8261C13.5608 14.8261 14.8261 13.5608 14.8261 12C14.8261 10.4392 13.5608 9.17392 12 9.17392C10.4392 9.17392 9.17391 10.4392 9.17391 12C9.17391 13.5608 10.4392 14.8261 12 14.8261Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]}),(0,M.jsxs)("g",{className:`${he.iconFade} ${t?he.hidden:he.visible}`,children:[(0,M.jsx)("path",{d:"M18.6025 9.28503C18.9174 8.9701 19.4364 8.99481 19.7015 9.35271C20.1484 9.95606 20.4943 10.507 20.7342 10.9199C21.134 11.6086 21.1329 12.4454 20.7303 13.1328C20.2144 14.013 19.2151 15.5225 17.7723 16.8193C16.3293 18.1162 14.3852 19.2497 12.0008 19.25C11.4192 19.25 10.8638 19.1823 10.3355 19.0613C9.77966 18.934 9.63498 18.2525 10.0382 17.8493C10.2412 17.6463 10.5374 17.573 10.8188 17.6302C11.1993 17.7076 11.5935 17.75 12.0008 17.75C13.8848 17.7497 15.4867 16.8568 16.7693 15.7041C18.0522 14.5511 18.9606 13.1867 19.4363 12.375C19.5656 12.1543 19.5659 11.8943 19.4373 11.6729C19.2235 11.3049 18.921 10.8242 18.5364 10.3003C18.3085 9.98991 18.3302 9.5573 18.6025 9.28503ZM12.0008 4.75C12.5814 4.75006 13.1358 4.81803 13.6632 4.93953C14.2182 5.06741 14.362 5.74812 13.9593 6.15091C13.7558 6.35435 13.4589 6.42748 13.1771 6.36984C12.7983 6.29239 12.4061 6.25006 12.0008 6.25C10.1167 6.25 8.51415 7.15145 7.23028 8.31543C5.94678 9.47919 5.03918 10.8555 4.56426 11.6729C4.43551 11.8945 4.43582 12.1542 4.56524 12.375C4.77587 12.7343 5.07189 13.2012 5.44718 13.7105C5.67623 14.0213 5.65493 14.4552 5.38193 14.7282C5.0671 15.0431 4.54833 15.0189 4.28292 14.6614C3.84652 14.0736 3.50813 13.5369 3.27129 13.1328C2.86831 12.4451 2.86717 11.6088 3.26739 10.9199C3.78185 10.0345 4.77959 8.51239 6.22247 7.2041C7.66547 5.89584 9.61202 4.75 12.0008 4.75Z",fill:"currentColor"}),(0,M.jsx)("path",{d:"M5 19L19 5",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})]})]}),tg=({size:e=24,isPaused:t=!1})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,M.jsxs)("g",{className:`${he.iconFadeFast} ${t?he.hidden:he.visible}`,children:[(0,M.jsx)("path",{d:"M8 6L8 18",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"}),(0,M.jsx)("path",{d:"M16 18L16 6",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round"})]}),(0,M.jsx)("path",{className:`${he.iconFadeFast} ${t?he.visible:he.hidden}`,d:"M17.75 10.701C18.75 11.2783 18.75 12.7217 17.75 13.299L8.75 18.4952C7.75 19.0725 6.5 18.3509 6.5 17.1962L6.5 6.80384C6.5 5.64914 7.75 4.92746 8.75 5.50481L17.75 10.701Z",stroke:"currentColor",strokeWidth:"1.5"})]});var ng=({size:e=16})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,M.jsx)("path",{d:"M10.6504 5.81117C10.9939 4.39628 13.0061 4.39628 13.3496 5.81117C13.5715 6.72517 14.6187 7.15891 15.4219 6.66952C16.6652 5.91193 18.0881 7.33479 17.3305 8.57815C16.8411 9.38134 17.2748 10.4285 18.1888 10.6504C19.6037 10.9939 19.6037 13.0061 18.1888 13.3496C17.2748 13.5715 16.8411 14.6187 17.3305 15.4219C18.0881 16.6652 16.6652 18.0881 15.4219 17.3305C14.6187 16.8411 13.5715 17.2748 13.3496 18.1888C13.0061 19.6037 10.9939 19.6037 10.6504 18.1888C10.4285 17.2748 9.38135 16.8411 8.57815 17.3305C7.33479 18.0881 5.91193 16.6652 6.66952 15.4219C7.15891 14.6187 6.72517 13.5715 5.81117 13.3496C4.39628 13.0061 4.39628 10.9939 5.81117 10.6504C6.72517 10.4285 7.15891 9.38134 6.66952 8.57815C5.91193 7.33479 7.33479 5.91192 8.57815 6.66952C9.38135 7.15891 10.4285 6.72517 10.6504 5.81117Z",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("circle",{cx:"12",cy:"12",r:"2.5",stroke:"currentColor",strokeWidth:"1.5"})]});var lg=({size:e=16})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:(0,M.jsx)("path",{d:"M13.5 4C14.7426 4 15.75 5.00736 15.75 6.25V7H18.5C18.9142 7 19.25 7.33579 19.25 7.75C19.25 8.16421 18.9142 8.5 18.5 8.5H17.9678L17.6328 16.2217C17.61 16.7475 17.5912 17.1861 17.5469 17.543C17.5015 17.9087 17.4225 18.2506 17.2461 18.5723C16.9747 19.0671 16.5579 19.4671 16.0518 19.7168C15.7227 19.8791 15.3772 19.9422 15.0098 19.9717C14.6514 20.0004 14.2126 20 13.6865 20H10.3135C9.78735 20 9.34856 20.0004 8.99023 19.9717C8.62278 19.9422 8.27729 19.8791 7.94824 19.7168C7.44205 19.4671 7.02532 19.0671 6.75391 18.5723C6.57751 18.2506 6.49853 17.9087 6.45312 17.543C6.40883 17.1861 6.39005 16.7475 6.36719 16.2217L6.03223 8.5H5.5C5.08579 8.5 4.75 8.16421 4.75 7.75C4.75 7.33579 5.08579 7 5.5 7H8.25V6.25C8.25 5.00736 9.25736 4 10.5 4H13.5ZM7.86621 16.1562C7.89013 16.7063 7.90624 17.0751 7.94141 17.3584C7.97545 17.6326 8.02151 17.7644 8.06934 17.8516C8.19271 18.0763 8.38239 18.2577 8.6123 18.3711C8.70153 18.4151 8.83504 18.4545 9.11035 18.4766C9.39482 18.4994 9.76335 18.5 10.3135 18.5H13.6865C14.2367 18.5 14.6052 18.4994 14.8896 18.4766C15.165 18.4545 15.2985 18.4151 15.3877 18.3711C15.6176 18.2577 15.8073 18.0763 15.9307 17.8516C15.9785 17.7644 16.0245 17.6326 16.0586 17.3584C16.0938 17.0751 16.1099 16.7063 16.1338 16.1562L16.4668 8.5H7.5332L7.86621 16.1562ZM9.97656 10.75C10.3906 10.7371 10.7371 11.0626 10.75 11.4766L10.875 15.4766C10.8879 15.8906 10.5624 16.2371 10.1484 16.25C9.73443 16.2629 9.38794 15.9374 9.375 15.5234L9.25 11.5234C9.23706 11.1094 9.56255 10.7629 9.97656 10.75ZM14.0244 10.75C14.4384 10.7635 14.7635 11.1105 14.75 11.5244L14.6201 15.5244C14.6066 15.9384 14.2596 16.2634 13.8457 16.25C13.4317 16.2365 13.1067 15.8896 13.1201 15.4756L13.251 11.4756C13.2645 11.0617 13.6105 10.7366 14.0244 10.75ZM10.5 5.5C10.0858 5.5 9.75 5.83579 9.75 6.25V7H14.25V6.25C14.25 5.83579 13.9142 5.5 13.5 5.5H10.5Z",fill:"currentColor"})});var dd=({size:e=16})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:[(0,M.jsxs)("g",{clipPath:"url(#clip0_2_53)",children:[(0,M.jsx)("path",{d:"M16.25 16.25L7.75 7.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M7.75 16.25L16.25 7.75",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})]}),(0,M.jsx)("defs",{children:(0,M.jsx)("clipPath",{id:"clip0_2_53",children:(0,M.jsx)("rect",{width:"24",height:"24",fill:"white"})})})]}),ag=({size:e=24})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",children:(0,M.jsx)("path",{d:"M16.7198 6.21973C17.0127 5.92683 17.4874 5.92683 17.7803 6.21973C18.0732 6.51262 18.0732 6.9874 17.7803 7.28027L13.0606 12L17.7803 16.7197C18.0732 17.0126 18.0732 17.4874 17.7803 17.7803C17.4875 18.0731 17.0127 18.0731 16.7198 17.7803L12.0001 13.0605L7.28033 17.7803C6.98746 18.0731 6.51268 18.0731 6.21979 17.7803C5.92689 17.4874 5.92689 17.0126 6.21979 16.7197L10.9395 12L6.21979 7.28027C5.92689 6.98738 5.92689 6.51262 6.21979 6.21973C6.51268 5.92683 6.98744 5.92683 7.28033 6.21973L12.0001 10.9395L16.7198 6.21973Z",fill:"currentColor"})}),og=({size:e=16})=>(0,M.jsxs)("svg",{width:e,height:e,viewBox:"0 0 20 20",fill:"none",children:[(0,M.jsx)("path",{d:"M9.99999 12.7082C11.4958 12.7082 12.7083 11.4956 12.7083 9.99984C12.7083 8.50407 11.4958 7.2915 9.99999 7.2915C8.50422 7.2915 7.29166 8.50407 7.29166 9.99984C7.29166 11.4956 8.50422 12.7082 9.99999 12.7082Z",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M10 3.9585V5.05698",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M10 14.9429V16.0414",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M5.7269 5.72656L6.50682 6.50649",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M13.4932 13.4932L14.2731 14.2731",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M3.95834 10H5.05683",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M14.9432 10H16.0417",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M5.7269 14.2731L6.50682 13.4932",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"}),(0,M.jsx)("path",{d:"M13.4932 6.50649L14.2731 5.72656",stroke:"currentColor",strokeWidth:"1.25",strokeLinecap:"round",strokeLinejoin:"round"})]}),ig=({size:e=16})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 20 20",fill:"none",children:(0,M.jsx)("path",{d:"M15.5 10.4955C15.4037 11.5379 15.0124 12.5314 14.3721 13.3596C13.7317 14.1878 12.8688 14.8165 11.8841 15.1722C10.8995 15.5278 9.83397 15.5957 8.81217 15.3679C7.79038 15.1401 6.8546 14.6259 6.11434 13.8857C5.37408 13.1454 4.85995 12.2096 4.63211 11.1878C4.40427 10.166 4.47215 9.10048 4.82781 8.11585C5.18346 7.13123 5.81218 6.26825 6.64039 5.62791C7.4686 4.98756 8.46206 4.59634 9.5045 4.5C8.89418 5.32569 8.60049 6.34302 8.67685 7.36695C8.75321 8.39087 9.19454 9.35339 9.92058 10.0794C10.6466 10.8055 11.6091 11.2468 12.6331 11.3231C13.657 11.3995 14.6743 11.1058 15.5 10.4955Z",stroke:"currentColor",strokeWidth:"1.13793",strokeLinecap:"round",strokeLinejoin:"round"})}),u5=({size:e=16})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,M.jsx)("path",{d:"M11.3799 6.9572L9.05645 4.63375M11.3799 6.9572L6.74949 11.5699C6.61925 11.6996 6.45577 11.791 6.277 11.8339L4.29549 12.3092C3.93194 12.3964 3.60478 12.0683 3.69297 11.705L4.16585 9.75693C4.20893 9.57947 4.29978 9.4172 4.42854 9.28771L9.05645 4.63375M11.3799 6.9572L12.3455 5.98759C12.9839 5.34655 12.9839 4.31002 12.3455 3.66897C11.7033 3.02415 10.6594 3.02415 10.0172 3.66897L9.06126 4.62892L9.05645 4.63375",stroke:"currentColor",strokeWidth:"0.9",strokeLinecap:"round",strokeLinejoin:"round"})}),sg=({size:e=24})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,M.jsx)("path",{d:"M13.5 4C14.7426 4 15.75 5.00736 15.75 6.25V7H18.5C18.9142 7 19.25 7.33579 19.25 7.75C19.25 8.16421 18.9142 8.5 18.5 8.5H17.9678L17.6328 16.2217C17.61 16.7475 17.5912 17.1861 17.5469 17.543C17.5015 17.9087 17.4225 18.2506 17.2461 18.5723C16.9747 19.0671 16.5579 19.4671 16.0518 19.7168C15.7227 19.8791 15.3772 19.9422 15.0098 19.9717C14.6514 20.0004 14.2126 20 13.6865 20H10.3135C9.78735 20 9.34856 20.0004 8.99023 19.9717C8.62278 19.9422 8.27729 19.8791 7.94824 19.7168C7.44205 19.4671 7.02532 19.0671 6.75391 18.5723C6.57751 18.2506 6.49853 17.9087 6.45312 17.543C6.40883 17.1861 6.39005 16.7475 6.36719 16.2217L6.03223 8.5H5.5C5.08579 8.5 4.75 8.16421 4.75 7.75C4.75 7.33579 5.08579 7 5.5 7H8.25V6.25C8.25 5.00736 9.25736 4 10.5 4H13.5ZM7.86621 16.1562C7.89013 16.7063 7.90624 17.0751 7.94141 17.3584C7.97545 17.6326 8.02151 17.7644 8.06934 17.8516C8.19271 18.0763 8.38239 18.2577 8.6123 18.3711C8.70153 18.4151 8.83504 18.4545 9.11035 18.4766C9.39482 18.4994 9.76335 18.5 10.3135 18.5H13.6865C14.2367 18.5 14.6052 18.4994 14.8896 18.4766C15.165 18.4545 15.2985 18.4151 15.3877 18.3711C15.6176 18.2577 15.8073 18.0763 15.9307 17.8516C15.9785 17.7644 16.0245 17.6326 16.0586 17.3584C16.0938 17.0751 16.1099 16.7063 16.1338 16.1562L16.4668 8.5H7.5332L7.86621 16.1562ZM9.97656 10.75C10.3906 10.7371 10.7371 11.0626 10.75 11.4766L10.875 15.4766C10.8879 15.8906 10.5624 16.2371 10.1484 16.25C9.73443 16.2629 9.38794 15.9374 9.375 15.5234L9.25 11.5234C9.23706 11.1094 9.56255 10.7629 9.97656 10.75ZM14.0244 10.75C14.4383 10.7635 14.7635 11.1105 14.75 11.5244L14.6201 15.5244C14.6066 15.9384 14.2596 16.2634 13.8457 16.25C13.4317 16.2365 13.1067 15.8896 13.1201 15.4756L13.251 11.4756C13.2645 11.0617 13.6105 10.7366 14.0244 10.75ZM10.5 5.5C10.0858 5.5 9.75 5.83579 9.75 6.25V7H14.25V6.25C14.25 5.83579 13.9142 5.5 13.5 5.5H10.5Z",fill:"currentColor"})}),ug=({size:e=16})=>(0,M.jsx)("svg",{width:e,height:e,viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,M.jsx)("path",{d:"M8.5 3.5L4 8L8.5 12.5",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})});var p5=["data-feedback-toolbar","data-annotation-popup","data-annotation-marker"],_d=p5.flatMap(e=>[`:not([${e}])`,`:not([${e}] *)`]).join(""),xd="feedback-freeze-styles",fd="__agentation_freeze";function cg(){if(typeof window>"u")return{frozen:!1,installed:!0,origSetTimeout:setTimeout,origSetInterval:setInterval,origRAF:t=>0,pausedAnimations:[],frozenTimeoutQueue:[],frozenRAFQueue:[]};let e=window;return e[fd]||(e[fd]={frozen:!1,installed:!1,origSetTimeout:null,origSetInterval:null,origRAF:null,pausedAnimations:[],frozenTimeoutQueue:[],frozenRAFQueue:[]}),e[fd]}var ne=cg();typeof window<"u"&&!ne.installed&&(ne.origSetTimeout=window.setTimeout.bind(window),ne.origSetInterval=window.setInterval.bind(window),ne.origRAF=window.requestAnimationFrame.bind(window),window.setTimeout=(e,t,...n)=>typeof e=="string"?ne.origSetTimeout(e,t):ne.origSetTimeout((...l)=>{ne.frozen?ne.frozenTimeoutQueue.push(()=>e(...l)):e(...l)},t,...n),window.setInterval=(e,t,...n)=>typeof e=="string"?ne.origSetInterval(e,t):ne.origSetInterval((...l)=>{ne.frozen||e(...l)},t,...n),window.requestAnimationFrame=e=>ne.origRAF(t=>{ne.frozen?ne.frozenRAFQueue.push(e):e(t)}),ne.installed=!0);var se=ne.origSetTimeout,rg=ne.origSetInterval;function dg(e){return e?p5.some(t=>!!e.closest?.(`[${t}]`)):!1}function _g(){if(typeof document>"u"||ne.frozen)return;ne.frozen=!0,ne.frozenTimeoutQueue=[],ne.frozenRAFQueue=[];let e=document.getElementById(xd);e||(e=document.createElement("style"),e.id=xd),e.textContent=`
    *${_d},
    *${_d}::before,
    *${_d}::after {
      animation-play-state: paused !important;
      transition: none !important;
    }
  `,document.head.appendChild(e),ne.pausedAnimations=[];try{document.getAnimations().forEach(t=>{if(t.playState!=="running")return;let n=t.effect?.target;dg(n)||(t.pause(),ne.pausedAnimations.push(t))})}catch{}document.querySelectorAll("video").forEach(t=>{t.paused||(t.dataset.wasPaused="false",t.pause())})}function c5(){if(typeof document>"u"||!ne.frozen)return;ne.frozen=!1;let e=ne.frozenTimeoutQueue;ne.frozenTimeoutQueue=[];for(let n of e)ne.origSetTimeout(()=>{if(ne.frozen){ne.frozenTimeoutQueue.push(n);return}try{n()}catch(l){console.warn("[agentation] Error replaying queued timeout:",l)}},0);let t=ne.frozenRAFQueue;ne.frozenRAFQueue=[];for(let n of t)ne.origRAF(l=>{if(ne.frozen){ne.frozenRAFQueue.push(n);return}n(l)});for(let n of ne.pausedAnimations)try{n.play()}catch(l){console.warn("[agentation] Error resuming animation:",l)}ne.pausedAnimations=[],document.getElementById(xd)?.remove(),document.querySelectorAll("video").forEach(n=>{n.dataset.wasPaused==="false"&&(n.play().catch(()=>{}),delete n.dataset.wasPaused)})}function md(e){if(!e)return;let t=n=>n.stopImmediatePropagation();document.addEventListener("focusin",t,!0),document.addEventListener("focusout",t,!0);try{e.focus()}finally{document.removeEventListener("focusin",t,!0),document.removeEventListener("focusout",t,!0)}}var r5=(0,Ae.forwardRef)(function({element:t,timestamp:n,selectedText:l,placeholder:a="What should change?",initialValue:o="",submitLabel:i="Add",onSubmit:s,onCancel:u,onDelete:h,style:y,accentColor:S="#3c82f7",isExiting:p=!1,lightMode:b=!1,computedStyles:A},k){let[G,f]=(0,Ae.useState)(o),[_,g]=(0,Ae.useState)(!1),[x,O]=(0,Ae.useState)("initial"),[le,L]=(0,Ae.useState)(!1),[U,W]=(0,Ae.useState)(!1),$=(0,Ae.useRef)(null),gt=(0,Ae.useRef)(null),Be=(0,Ae.useRef)(null),on=(0,Ae.useRef)(null);(0,Ae.useEffect)(()=>{p&&x!=="exit"&&O("exit")},[p,x]),(0,Ae.useEffect)(()=>{se(()=>{O("enter")},0);let be=se(()=>{O("entered")},200),fl=se(()=>{let Gt=$.current;Gt&&(md(Gt),Gt.selectionStart=Gt.selectionEnd=Gt.value.length,Gt.scrollTop=Gt.scrollHeight)},50);return()=>{clearTimeout(be),clearTimeout(fl),Be.current&&clearTimeout(Be.current),on.current&&clearTimeout(on.current)}},[]);let pt=(0,Ae.useCallback)(()=>{on.current&&clearTimeout(on.current),g(!0),on.current=se(()=>{g(!1),md($.current)},250)},[]);(0,Ae.useImperativeHandle)(k,()=>({shake:pt}),[pt]);let Xt=(0,Ae.useCallback)(()=>{O("exit"),Be.current=se(()=>{u()},150)},[u]),Xl=(0,Ae.useCallback)(()=>{G.trim()&&s(G.trim())},[G,s]),uu=(0,Ae.useCallback)(be=>{be.stopPropagation(),!be.nativeEvent.isComposing&&(be.key==="Enter"&&!be.shiftKey&&(be.preventDefault(),Xl()),be.key==="Escape"&&Xt())},[Xl,Xt]),D=[pe.popup,b?pe.light:"",x==="enter"?pe.enter:"",x==="entered"?pe.entered:"",x==="exit"?pe.exit:"",_?pe.shake:""].filter(Boolean).join(" ");return(0,ke.jsxs)("div",{ref:gt,className:D,"data-annotation-popup":!0,style:y,onClick:be=>be.stopPropagation(),children:[(0,ke.jsxs)("div",{className:pe.header,children:[A&&Object.keys(A).length>0?(0,ke.jsxs)("button",{className:pe.headerToggle,onClick:()=>{let be=U;W(!U),be&&se(()=>md($.current),0)},type:"button",children:[(0,ke.jsx)("svg",{className:`${pe.chevron} ${U?pe.expanded:""}`,width:"14",height:"14",viewBox:"0 0 14 14",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,ke.jsx)("path",{d:"M5.5 10.25L9 7.25L5.75 4",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})}),(0,ke.jsx)("span",{className:pe.element,children:t})]}):(0,ke.jsx)("span",{className:pe.element,children:t}),n&&(0,ke.jsx)("span",{className:pe.timestamp,children:n})]}),A&&Object.keys(A).length>0&&(0,ke.jsx)("div",{className:`${pe.stylesWrapper} ${U?pe.expanded:""}`,children:(0,ke.jsx)("div",{className:pe.stylesInner,children:(0,ke.jsx)("div",{className:pe.stylesBlock,children:Object.entries(A).map(([be,fl])=>(0,ke.jsxs)("div",{className:pe.styleLine,children:[(0,ke.jsx)("span",{className:pe.styleProperty,children:be.replace(/([A-Z])/g,"-$1").toLowerCase()}),": ",(0,ke.jsx)("span",{className:pe.styleValue,children:fl}),";"]},be))})})}),l&&(0,ke.jsxs)("div",{className:pe.quote,children:["\u201C",l.slice(0,80),l.length>80?"...":"","\u201D"]}),(0,ke.jsx)("textarea",{ref:$,className:pe.textarea,style:{borderColor:le?S:void 0},placeholder:a,value:G,onChange:be=>f(be.target.value),onFocus:()=>L(!0),onBlur:()=>L(!1),rows:2,onKeyDown:uu}),(0,ke.jsxs)("div",{className:pe.actions,children:[h&&(0,ke.jsx)("div",{className:pe.deleteWrapper,children:(0,ke.jsx)("button",{className:pe.deleteButton,onClick:h,type:"button",children:(0,ke.jsx)(sg,{size:22})})}),(0,ke.jsx)("button",{className:pe.cancel,onClick:Xt,children:"Cancel"}),(0,ke.jsx)("button",{className:pe.submit,style:{backgroundColor:S,opacity:G.trim()?1:.4},onClick:Xl,disabled:!G.trim(),children:i})]})]})});function Za(e){if(e.parentElement)return e.parentElement;let t=e.getRootNode();return t instanceof ShadowRoot?t.host:null}function yt(e,t){let n=e;for(;n;){if(n.matches(t))return n;n=Za(n)}return null}function fg(e,t=4){let n=[],l=e,a=0;for(;l&&a<t;){let o=l.tagName.toLowerCase();if(o==="html"||o==="body")break;let i=o;if(l.id)i=`#${l.id}`;else if(l.className&&typeof l.className=="string"){let u=l.className.split(/\s+/).find(h=>h.length>2&&!h.match(/^[a-z]{1,2}$/)&&!h.match(/[A-Z0-9]{5,}/));u&&(i=`.${u.split("_")[0]}`)}let s=Za(l);!l.parentElement&&s&&(i=`\u27E8shadow\u27E9 ${i}`),n.unshift(i),l=s,a++}return n.join(" > ")}function iu(e){let t=fg(e);if(e.dataset.element)return{name:e.dataset.element,path:t};let n=e.tagName.toLowerCase();if(["path","circle","rect","line","g"].includes(n)){let l=yt(e,"svg");if(l){let a=Za(l);if(a instanceof HTMLElement)return{name:`graphic in ${iu(a).name}`,path:t}}return{name:"graphic element",path:t}}if(n==="svg"){let l=Za(e);if(l?.tagName.toLowerCase()==="button"){let a=l.textContent?.trim();return{name:a?`icon in "${a}" button`:"button icon",path:t}}return{name:"icon",path:t}}if(n==="button"){let l=e.textContent?.trim(),a=e.getAttribute("aria-label");return a?{name:`button [${a}]`,path:t}:{name:l?`button "${l.slice(0,25)}"`:"button",path:t}}if(n==="a"){let l=e.textContent?.trim(),a=e.getAttribute("href");return l?{name:`link "${l.slice(0,25)}"`,path:t}:a?{name:`link to ${a.slice(0,30)}`,path:t}:{name:"link",path:t}}if(n==="input"){let l=e.getAttribute("type")||"text",a=e.getAttribute("placeholder"),o=e.getAttribute("name");return a?{name:`input "${a}"`,path:t}:o?{name:`input [${o}]`,path:t}:{name:`${l} input`,path:t}}if(["h1","h2","h3","h4","h5","h6"].includes(n)){let l=e.textContent?.trim();return{name:l?`${n} "${l.slice(0,35)}"`:n,path:t}}if(n==="p"){let l=e.textContent?.trim();return l?{name:`paragraph: "${l.slice(0,40)}${l.length>40?"...":""}"`,path:t}:{name:"paragraph",path:t}}if(n==="span"||n==="label"){let l=e.textContent?.trim();return l&&l.length<40?{name:`"${l}"`,path:t}:{name:n,path:t}}if(n==="li"){let l=e.textContent?.trim();return l&&l.length<40?{name:`list item: "${l.slice(0,35)}"`,path:t}:{name:"list item",path:t}}if(n==="blockquote")return{name:"blockquote",path:t};if(n==="code"){let l=e.textContent?.trim();return l&&l.length<30?{name:`code: \`${l}\``,path:t}:{name:"code",path:t}}if(n==="pre")return{name:"code block",path:t};if(n==="img"){let l=e.getAttribute("alt");return{name:l?`image "${l.slice(0,30)}"`:"image",path:t}}if(n==="video")return{name:"video",path:t};if(["div","section","article","nav","header","footer","aside","main"].includes(n)){let l=e.className,a=e.getAttribute("role"),o=e.getAttribute("aria-label");if(o)return{name:`${n} [${o}]`,path:t};if(a)return{name:`${a}`,path:t};if(typeof l=="string"&&l){let i=l.split(/[\s_-]+/).map(s=>s.replace(/[A-Z0-9]{5,}.*$/,"")).filter(s=>s.length>2&&!/^[a-z]{1,2}$/.test(s)).slice(0,2);if(i.length>0)return{name:i.join(" "),path:t}}return{name:n==="div"?"container":n,path:t}}return{name:n,path:t}}function ni(e){let t=[],n=e.textContent?.trim();n&&n.length<100&&t.push(n);let l=e.previousElementSibling;if(l){let o=l.textContent?.trim();o&&o.length<50&&t.unshift(`[before: "${o.slice(0,40)}"]`)}let a=e.nextElementSibling;if(a){let o=a.textContent?.trim();o&&o.length<50&&t.push(`[after: "${o.slice(0,40)}"]`)}return t.join(" ")}function Fs(e){let t=Za(e);if(!t)return"";let a=(e.getRootNode()instanceof ShadowRoot&&e.parentElement?Array.from(e.parentElement.children):Array.from(t.children)).filter(y=>y!==e&&y instanceof HTMLElement);if(a.length===0)return"";let o=a.slice(0,4).map(y=>{let S=y.tagName.toLowerCase(),p=y.className,b="";if(typeof p=="string"&&p){let A=p.split(/\s+/).map(k=>k.replace(/[_][a-zA-Z0-9]{5,}.*$/,"")).find(k=>k.length>2&&!/^[a-z]{1,2}$/.test(k));A&&(b=`.${A}`)}if(S==="button"||S==="a"){let A=y.textContent?.trim().slice(0,15);if(A)return`${S}${b} "${A}"`}return`${S}${b}`}),s=t.tagName.toLowerCase();if(typeof t.className=="string"&&t.className){let y=t.className.split(/\s+/).map(S=>S.replace(/[_][a-zA-Z0-9]{5,}.*$/,"")).find(S=>S.length>2&&!/^[a-z]{1,2}$/.test(S));y&&(s=`.${y}`)}let u=t.children.length,h=u>o.length+1?` (${u} total in ${s})`:"";return o.join(", ")+h}function li(e){let t=e.className;return typeof t!="string"||!t?"":t.split(/\s+/).filter(l=>l.length>0).map(l=>{let a=l.match(/^([a-zA-Z][a-zA-Z0-9_-]*?)(?:_[a-zA-Z0-9]{5,})?$/);return a?a[1]:l}).filter((l,a,o)=>o.indexOf(l)===a).join(", ")}var b5=new Set(["none","normal","auto","0px","rgba(0, 0, 0, 0)","transparent","static","visible"]),mg=new Set(["p","span","h1","h2","h3","h4","h5","h6","label","li","td","th","blockquote","figcaption","caption","legend","dt","dd","pre","code","em","strong","b","i","a","time","cite","q"]),hg=new Set(["input","textarea","select"]),yg=new Set(["img","video","canvas","svg"]),gg=new Set(["div","section","article","nav","header","footer","aside","main","ul","ol","form","fieldset"]);function Ps(e){if(typeof window>"u")return{};let t=window.getComputedStyle(e),n={},l=e.tagName.toLowerCase(),a;mg.has(l)?a=["color","fontSize","fontWeight","fontFamily","lineHeight"]:l==="button"||l==="a"&&e.getAttribute("role")==="button"?a=["backgroundColor","color","padding","borderRadius","fontSize"]:hg.has(l)?a=["backgroundColor","color","padding","borderRadius","fontSize"]:yg.has(l)?a=["width","height","objectFit","borderRadius"]:gg.has(l)?a=["display","padding","margin","gap","backgroundColor"]:a=["color","fontSize","margin","padding","backgroundColor"];for(let o of a){let i=o.replace(/([A-Z])/g,"-$1").toLowerCase(),s=t.getPropertyValue(i);s&&!b5.has(s)&&(n[o]=s)}return n}var pg=["color","backgroundColor","borderColor","fontSize","fontWeight","fontFamily","lineHeight","letterSpacing","textAlign","width","height","padding","margin","border","borderRadius","display","position","top","right","bottom","left","zIndex","flexDirection","justifyContent","alignItems","gap","opacity","visibility","overflow","boxShadow","transform"];function eu(e){if(typeof window>"u")return"";let t=window.getComputedStyle(e),n=[];for(let l of pg){let a=l.replace(/([A-Z])/g,"-$1").toLowerCase(),o=t.getPropertyValue(a);o&&!b5.has(o)&&n.push(`${a}: ${o}`)}return n.join("; ")}function bg(e){if(!e)return;let t={},n=e.split(";").map(l=>l.trim()).filter(Boolean);for(let l of n){let a=l.indexOf(":");if(a>0){let o=l.slice(0,a).trim(),i=l.slice(a+1).trim();o&&i&&(t[o]=i)}}return Object.keys(t).length>0?t:void 0}function tu(e){let t=[],n=e.getAttribute("role"),l=e.getAttribute("aria-label"),a=e.getAttribute("aria-describedby"),o=e.getAttribute("tabindex"),i=e.getAttribute("aria-hidden");return n&&t.push(`role="${n}"`),l&&t.push(`aria-label="${l}"`),a&&t.push(`aria-describedby="${a}"`),o&&t.push(`tabindex=${o}`),i==="true"&&t.push("aria-hidden"),e.matches("a, button, input, select, textarea, [tabindex]")&&t.push("focusable"),t.join(", ")}function nu(e){let t=[],n=e;for(;n&&n.tagName.toLowerCase()!=="html";){let l=n.tagName.toLowerCase(),a=l;if(n.id)a=`${l}#${n.id}`;else if(n.className&&typeof n.className=="string"){let i=n.className.split(/\s+/).map(s=>s.replace(/[_][a-zA-Z0-9]{5,}.*$/,"")).find(s=>s.length>2);i&&(a=`${l}.${i}`)}let o=Za(n);!n.parentElement&&o&&(a=`\u27E8shadow\u27E9 ${a}`),t.unshift(a),n=o}return t.join(" > ")}var Cd="feedback-annotations-",v5=7;function su(e){return`${Cd}${e}`}function hd(e){if(typeof window>"u")return[];try{let t=localStorage.getItem(su(e));if(!t)return[];let n=JSON.parse(t),l=Date.now()-v5*24*60*60*1e3;return n.filter(a=>!a.timestamp||a.timestamp>l)}catch{return[]}}function S5(e,t){if(!(typeof window>"u"))try{localStorage.setItem(su(e),JSON.stringify(t))}catch{}}function vg(){let e=new Map;if(typeof window>"u")return e;try{let t=Date.now()-v5*24*60*60*1e3;for(let n=0;n<localStorage.length;n++){let l=localStorage.key(n);if(l?.startsWith(Cd)){let a=l.slice(Cd.length),o=localStorage.getItem(l);if(o){let s=JSON.parse(o).filter(u=>!u.timestamp||u.timestamp>t);s.length>0&&e.set(a,s)}}}}catch{}return e}function ai(e,t,n){let l=t.map(a=>({...a,_syncedTo:n}));S5(e,l)}var x5="agentation-session-";function Td(e){return`${x5}${e}`}function Sg(e){if(typeof window>"u")return null;try{return localStorage.getItem(Td(e))}catch{return null}}function yd(e,t){if(!(typeof window>"u"))try{localStorage.setItem(Td(e),t)}catch{}}function xg(e){if(!(typeof window>"u"))try{localStorage.removeItem(Td(e))}catch{}}var wd=`${x5}toolbar-hidden`;function Cg(){if(typeof window>"u")return!1;try{return sessionStorage.getItem(wd)==="1"}catch{return!1}}function wg(e){if(!(typeof window>"u"))try{e?sessionStorage.setItem(wd,"1"):sessionStorage.removeItem(wd)}catch{}}async function gd(e,t){let n=await fetch(`${e}/sessions`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url:t})});if(!n.ok)throw new Error(`Failed to create session: ${n.status}`);return n.json()}async function d5(e,t){let n=await fetch(`${e}/sessions/${t}`);if(!n.ok)throw new Error(`Failed to get session: ${n.status}`);return n.json()}async function lu(e,t,n){let l=await fetch(`${e}/sessions/${t}/annotations`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)});if(!l.ok)throw new Error(`Failed to sync annotation: ${l.status}`);return l.json()}async function Eg(e,t,n){let l=await fetch(`${e}/annotations/${t}`,{method:"PATCH",headers:{"Content-Type":"application/json"},body:JSON.stringify(n)});if(!l.ok)throw new Error(`Failed to update annotation: ${l.status}`);return l.json()}async function _5(e,t){let n=await fetch(`${e}/annotations/${t}`,{method:"DELETE"});if(!n.ok)throw new Error(`Failed to delete annotation: ${n.status}`)}var re={FunctionComponent:0,ClassComponent:1,IndeterminateComponent:2,HostRoot:3,HostPortal:4,HostComponent:5,HostText:6,Fragment:7,Mode:8,ContextConsumer:9,ContextProvider:10,ForwardRef:11,Profiler:12,SuspenseComponent:13,MemoComponent:14,SimpleMemoComponent:15,LazyComponent:16,IncompleteClassComponent:17,DehydratedFragment:18,SuspenseListComponent:19,ScopeComponent:21,OffscreenComponent:22,LegacyHiddenComponent:23,CacheComponent:24,TracingMarkerComponent:25,HostHoistable:26,HostSingleton:27,IncompleteFunctionComponent:28,Throw:29,ViewTransitionComponent:30,ActivityComponent:31},f5=new Set(["Component","PureComponent","Fragment","Suspense","Profiler","StrictMode","Routes","Route","Outlet","Root","ErrorBoundaryHandler","HotReload","Hot"]),m5=[/Boundary$/,/BoundaryHandler$/,/Provider$/,/Consumer$/,/^(Inner|Outer)/,/Router$/,/^Client(Page|Segment|Root)/,/^Segment(ViewNode|Node)$/,/^LayoutSegment/,/^Server(Root|Component|Render)/,/^RSC/,/Context$/,/^Hot(Reload)?$/,/^(Dev|React)(Overlay|Tools|Root)/,/Overlay$/,/Handler$/,/^With[A-Z]/,/Wrapper$/,/^Root$/],Tg=[/Page$/,/View$/,/Screen$/,/Section$/,/Card$/,/List$/,/Item$/,/Form$/,/Modal$/,/Dialog$/,/Button$/,/Nav$/,/Header$/,/Footer$/,/Layout$/,/Panel$/,/Tab$/,/Menu$/];function kg(e){let t=e?.mode??"filtered",n=f5;if(e?.skipExact){let l=e.skipExact instanceof Set?e.skipExact:new Set(e.skipExact);n=new Set([...f5,...l])}return{maxComponents:e?.maxComponents??6,maxDepth:e?.maxDepth??30,mode:t,skipExact:n,skipPatterns:e?.skipPatterns?[...m5,...e.skipPatterns]:m5,userPatterns:e?.userPatterns??Tg,filter:e?.filter}}function Mg(e){return e.replace(/([a-z])([A-Z])/g,"$1-$2").replace(/([A-Z])([A-Z][a-z])/g,"$1-$2").toLowerCase()}function Ag(e,t=10){let n=new Set,l=e,a=0;for(;l&&a<t;)l.className&&typeof l.className=="string"&&l.className.split(/\s+/).forEach(o=>{if(o.length>1){let i=o.replace(/[_][a-zA-Z0-9]{5,}.*$/,"").toLowerCase();i.length>1&&n.add(i)}}),l=l.parentElement,a++;return n}function zg(e,t){let n=Mg(e);for(let l of t){if(l===n)return!0;let a=n.split("-").filter(i=>i.length>2),o=l.split("-").filter(i=>i.length>2);for(let i of a)for(let s of o)if(i===s||i.includes(s)||s.includes(i))return!0}return!1}function Ng(e,t,n,l){if(n.filter)return n.filter(e,t);switch(n.mode){case"all":return!0;case"filtered":return!(n.skipExact.has(e)||n.skipPatterns.some(a=>a.test(e)));case"smart":return n.skipExact.has(e)||n.skipPatterns.some(a=>a.test(e))?!1:!!(l&&zg(e,l)||n.userPatterns.some(a=>a.test(e)));default:return!0}}var qa=null,Lg=new WeakMap;function pd(e){return Object.keys(e).some(t=>t.startsWith("__reactFiber$")||t.startsWith("__reactInternalInstance$")||t.startsWith("__reactProps$"))}function Og(){if(qa!==null)return qa;if(typeof document>"u")return!1;if(document.body&&pd(document.body))return qa=!0,!0;let e=["#root","#app","#__next","[data-reactroot]"];for(let t of e){let n=document.querySelector(t);if(n&&pd(n))return qa=!0,!0}if(document.body){for(let t of document.body.children)if(pd(t))return qa=!0,!0}return qa=!1,!1}var oi={map:Lg};function Dg(e){return Object.keys(e).find(n=>n.startsWith("__reactFiber$")||n.startsWith("__reactInternalInstance$"))||null}function Bg(e){let t=Dg(e);return t?e[t]:null}function jl(e){return e?e.displayName?e.displayName:e.name?e.name:null:null}function Hg(e){let{tag:t,type:n,elementType:l}=e;if(t===re.HostComponent||t===re.HostText||t===re.HostHoistable||t===re.HostSingleton||t===re.Fragment||t===re.Mode||t===re.Profiler||t===re.DehydratedFragment||t===re.HostRoot||t===re.HostPortal||t===re.ScopeComponent||t===re.OffscreenComponent||t===re.LegacyHiddenComponent||t===re.CacheComponent||t===re.TracingMarkerComponent||t===re.Throw||t===re.ViewTransitionComponent||t===re.ActivityComponent)return null;if(t===re.ForwardRef){let a=l;if(a?.render){let o=jl(a.render);if(o)return o}return a?.displayName?a.displayName:jl(n)}if(t===re.MemoComponent||t===re.SimpleMemoComponent){let a=l;if(a?.type){let o=jl(a.type);if(o)return o}return a?.displayName?a.displayName:jl(n)}if(t===re.ContextProvider){let a=n;return a?._context?.displayName?`${a._context.displayName}.Provider`:null}if(t===re.ContextConsumer){let a=n;return a?.displayName?`${a.displayName}.Consumer`:null}if(t===re.LazyComponent){let a=l;return a?._status===1&&a._result?jl(a._result):null}return t===re.SuspenseComponent||t===re.SuspenseListComponent?null:t===re.IncompleteClassComponent||t===re.IncompleteFunctionComponent||t===re.FunctionComponent||t===re.ClassComponent||t===re.IndeterminateComponent?jl(n):null}function Yg(e){return e.length<=2||e.length<=3&&e===e.toLowerCase()}function Rg(e,t){let n=kg(t),l=n.mode==="all";if(l){let u=oi.map.get(e);if(u!==void 0)return u}if(!Og()){let u={path:null,components:[]};return l&&oi.map.set(e,u),u}let a=n.mode==="smart"?Ag(e):void 0,o=[];try{let u=Bg(e),h=0;for(;u&&h<n.maxDepth&&o.length<n.maxComponents;){let y=Hg(u);y&&!Yg(y)&&Ng(y,h,n,a)&&o.push(y),u=u.return,h++}}catch{let u={path:null,components:[]};return l&&oi.map.set(e,u),u}if(o.length===0){let u={path:null,components:[]};return l&&oi.map.set(e,u),u}let s={path:o.slice().reverse().map(u=>`<${u}>`).join(" "),components:o};return l&&oi.map.set(e,s),s}var ii={FunctionComponent:0,ClassComponent:1,IndeterminateComponent:2,HostRoot:3,HostPortal:4,HostComponent:5,HostText:6,Fragment:7,Mode:8,ContextConsumer:9,ContextProvider:10,ForwardRef:11,Profiler:12,SuspenseComponent:13,MemoComponent:14,SimpleMemoComponent:15,LazyComponent:16};function Ug(e){if(!e||typeof e!="object")return null;let t=Object.keys(e),n=t.find(o=>o.startsWith("__reactFiber$"));if(n)return e[n]||null;let l=t.find(o=>o.startsWith("__reactInternalInstance$"));if(l)return e[l]||null;let a=t.find(o=>{if(!o.startsWith("__react"))return!1;let i=e[o];return i&&typeof i=="object"&&"_debugSource"in i});return a&&e[a]||null}function ui(e){if(!e.type||typeof e.type=="string")return null;if(typeof e.type=="object"||typeof e.type=="function"){let t=e.type;if(t.displayName)return t.displayName;if(t.name)return t.name}return null}function jg(e,t=50){let n=e,l=0;for(;n&&l<t;){if(n._debugSource)return{source:n._debugSource,componentName:ui(n)};if(n._debugOwner?._debugSource)return{source:n._debugOwner._debugSource,componentName:ui(n._debugOwner)};n=n.return,l++}return null}function Xg(e){let t=e,n=0,l=50;for(;t&&n<l;){let a=t,o=["_debugSource","__source","_source","debugSource"];for(let i of o){let s=a[i];if(s&&typeof s=="object"&&"fileName"in s)return{source:s,componentName:ui(t)}}if(t.memoizedProps){let i=t.memoizedProps;if(i.__source&&typeof i.__source=="object"){let s=i.__source;if(s.fileName&&s.lineNumber)return{source:{fileName:s.fileName,lineNumber:s.lineNumber,columnNumber:s.columnNumber},componentName:ui(t)}}}t=t.return,n++}return null}var au=new Map;function Qg(e){let t=e.tag,n=e.type,l=e.elementType;if(typeof n=="string"||n==null||typeof n=="function"&&n.prototype?.isReactComponent)return null;if((t===ii.FunctionComponent||t===ii.IndeterminateComponent)&&typeof n=="function")return n;if(t===ii.ForwardRef&&l){let a=l.render;if(typeof a=="function")return a}if((t===ii.MemoComponent||t===ii.SimpleMemoComponent)&&l){let a=l.type;if(typeof a=="function")return a}return typeof n=="function"?n:null}function qg(){let e=C5.default,t=e.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;if(t&&"H"in t)return{get:()=>t.H,set:l=>{t.H=l}};let n=e.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;if(n){let l=n.ReactCurrentDispatcher;if(l&&"current"in l)return{get:()=>l.current,set:a=>{l.current=a}}}return null}function $g(e){let t=e.split(`
`),n=[/source-location/,/\/dist\/index\./,/node_modules\//,/react-dom/,/react\.development/,/react\.production/,/chunk-[A-Z0-9]+/i,/react-stack-bottom-frame/,/react-reconciler/,/scheduler/,/<anonymous>/],l=/^\s*at\s+(?:.*?\s+\()?(.+?):(\d+):(\d+)\)?$/,a=/^[^@]*@(.+?):(\d+):(\d+)$/;for(let o of t){let i=o.trim();if(!i||n.some(u=>u.test(i)))continue;let s=l.exec(i)||a.exec(i);if(s)return{fileName:s[1],line:parseInt(s[2],10),column:parseInt(s[3],10)}}return null}function Zg(e){let t=e;return t=t.replace(/[?#].*$/,""),t=t.replace(/^turbopack:\/\/\/\[project\]\//,""),t=t.replace(/^webpack-internal:\/\/\/\.\//,""),t=t.replace(/^webpack-internal:\/\/\//,""),t=t.replace(/^webpack:\/\/\/\.\//,""),t=t.replace(/^webpack:\/\/\//,""),t=t.replace(/^turbopack:\/\/\//,""),t=t.replace(/^https?:\/\/[^/]+\//,""),t=t.replace(/^file:\/\/\//,"/"),t=t.replace(/^\([^)]+\)\/\.\//,""),t=t.replace(/^\.\//,""),t}function Gg(e){let t=Qg(e);if(!t)return null;if(au.has(t))return au.get(t);let n=qg();if(!n)return au.set(t,null),null;let l=n.get(),a=null;try{let o=new Proxy({},{get(){throw new Error("probe")}});n.set(o);try{t({})}catch(i){if(i instanceof Error&&i.message==="probe"&&i.stack){let s=$g(i.stack);s&&(a={fileName:Zg(s.fileName),lineNumber:s.line,columnNumber:s.column,componentName:ui(e)||void 0})}}}finally{n.set(l)}return au.set(t,a),a}function Vg(e,t=15){let n=e,l=0;for(;n&&l<t;){let a=Gg(n);if(a)return a;n=n.return,l++}return null}function Ed(e){let t=Ug(e);if(!t)return{found:!1,reason:"no-fiber",isReactApp:!1,isProduction:!1};let n=jg(t);if(n||(n=Xg(t)),n?.source)return{found:!0,source:{fileName:n.source.fileName,lineNumber:n.source.lineNumber,columnNumber:n.source.columnNumber,componentName:n.componentName||void 0},isReactApp:!0,isProduction:!1};let l=Vg(t);return l?{found:!0,source:l,isReactApp:!0,isProduction:!1}:{found:!1,reason:"no-debug-source",isReactApp:!0,isProduction:!1}}function Kg(e,t="path"){let{fileName:n,lineNumber:l,columnNumber:a}=e,o=`${n}:${l}`;return a!==void 0&&(o+=`:${a}`),t==="vscode"?`vscode://file${n.startsWith("/")?"":"/"}${o}`:o}function Jg(e,t=10){let n=e,l=0;for(;n&&l<t;){let a=Ed(n);if(a.found)return a;n=n.parentElement,l++}return Ed(e)}var Wg=`.styles-module__toolbar___wNsdK svg[fill=none],
.styles-module__markersLayer___-25j1 svg[fill=none],
.styles-module__fixedMarkersLayer___ffyX6 svg[fill=none] {
  fill: none !important;
}
.styles-module__toolbar___wNsdK svg[fill=none] :not([fill]),
.styles-module__markersLayer___-25j1 svg[fill=none] :not([fill]),
.styles-module__fixedMarkersLayer___ffyX6 svg[fill=none] :not([fill]) {
  fill: none !important;
}

.styles-module__toolbar___wNsdK :where(button, input, select, textarea, label) {
  background: unset;
  border: unset;
  border-radius: unset;
  padding: unset;
  margin: unset;
  color: unset;
  font: unset;
  letter-spacing: unset;
  text-transform: unset;
  text-decoration: unset;
  box-shadow: unset;
  outline: unset;
}

@keyframes styles-module__toolbarEnter___u8RRu {
  from {
    opacity: 0;
    transform: scale(0.5) rotate(90deg);
  }
  to {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}
@keyframes styles-module__toolbarHide___y8kaT {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.8);
  }
}
@keyframes styles-module__badgeEnter___mVQLj {
  from {
    opacity: 0;
    transform: scale(0);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__scaleIn___c-r1K {
  from {
    opacity: 0;
    transform: scale(0.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__scaleOut___Wctwz {
  from {
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(0.85);
  }
}
@keyframes styles-module__slideUp___kgD36 {
  from {
    opacity: 0;
    transform: scale(0.85) translateY(8px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
@keyframes styles-module__slideDown___zcdje {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.85) translateY(8px);
  }
}
@keyframes styles-module__markerIn___5FaAP {
  0% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.3);
  }
  100% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
}
@keyframes styles-module__markerOut___GU5jX {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.3);
  }
}
@keyframes styles-module__fadeIn___b9qmf {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes styles-module__fadeOut___6Ut6- {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
@keyframes styles-module__tooltipIn___0N31w {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(2px) scale(0.891);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0) scale(0.909);
  }
}
@keyframes styles-module__hoverHighlightIn___6WYHY {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
@keyframes styles-module__hoverTooltipIn___FYGQx {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(4px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
@keyframes styles-module__settingsPanelIn___MGfO8 {
  from {
    opacity: 0;
    transform: translateY(10px) scale(0.95);
    filter: blur(5px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0px);
  }
}
@keyframes styles-module__settingsPanelOut___Zfymi {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0px);
  }
  to {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
    filter: blur(5px);
  }
}
.styles-module__toolbar___wNsdK {
  position: fixed;
  bottom: 1.25rem;
  right: 1.25rem;
  width: 297px;
  z-index: 100000;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  pointer-events: none;
  transition: left 0s, top 0s, right 0s, bottom 0s;
}

.styles-module__toolbarContainer___dIhma {
  user-select: none;
  margin-left: auto;
  align-self: flex-end;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a1a1a;
  color: #fff;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2), 0 4px 16px rgba(0, 0, 0, 0.1);
  pointer-events: auto;
  cursor: grab;
  transition: width 0.4s cubic-bezier(0.19, 1, 0.22, 1), transform 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__toolbarContainer___dIhma.styles-module__dragging___xrolZ {
  transition: width 0.4s cubic-bezier(0.19, 1, 0.22, 1);
  cursor: grabbing;
}
.styles-module__toolbarContainer___dIhma.styles-module__entrance___sgHd8 {
  animation: styles-module__toolbarEnter___u8RRu 0.5s cubic-bezier(0.34, 1.2, 0.64, 1) forwards;
}
.styles-module__toolbarContainer___dIhma.styles-module__hiding___1td44 {
  animation: styles-module__toolbarHide___y8kaT 0.4s cubic-bezier(0.4, 0, 1, 1) forwards;
  pointer-events: none;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn {
  width: 44px;
  height: 44px;
  border-radius: 22px;
  padding: 0;
  cursor: pointer;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn svg {
  margin-top: -1px;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn:hover {
  background: #2a2a2a;
}
.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn:active {
  transform: scale(0.95);
}
.styles-module__toolbarContainer___dIhma.styles-module__expanded___ofKPx {
  height: 44px;
  border-radius: 1.5rem;
  padding: 0.375rem;
  width: 257px;
}
.styles-module__toolbarContainer___dIhma.styles-module__expanded___ofKPx.styles-module__serverConnected___Gfbou {
  width: 297px;
}

.styles-module__toggleContent___0yfyP {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.1s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__toggleContent___0yfyP.styles-module__visible___KHwEW {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}
.styles-module__toggleContent___0yfyP.styles-module__hidden___Ae8H4 {
  opacity: 0;
  pointer-events: none;
}

.styles-module__controlsContent___9GJWU {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  transition: filter 0.8s cubic-bezier(0.19, 1, 0.22, 1), opacity 0.8s cubic-bezier(0.19, 1, 0.22, 1), transform 0.6s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__controlsContent___9GJWU.styles-module__visible___KHwEW {
  opacity: 1;
  filter: blur(0px);
  transform: scale(1);
  visibility: visible;
  pointer-events: auto;
}
.styles-module__controlsContent___9GJWU.styles-module__hidden___Ae8H4 {
  pointer-events: none;
  opacity: 0;
  filter: blur(10px);
  transform: scale(0.4);
}

.styles-module__badge___2XsgF {
  position: absolute;
  top: -13px;
  right: -13px;
  user-select: none;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: #3c82f7;
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.15), inset 0 0 0 1px rgba(255, 255, 255, 0.04);
  opacity: 1;
  transition: transform 0.3s ease, opacity 0.2s ease;
  transform: scale(1);
}
.styles-module__badge___2XsgF.styles-module__fadeOut___6Ut6- {
  opacity: 0;
  transform: scale(0);
  pointer-events: none;
}
.styles-module__badge___2XsgF.styles-module__entrance___sgHd8 {
  animation: styles-module__badgeEnter___mVQLj 0.3s cubic-bezier(0.34, 1.2, 0.64, 1) 0.4s both;
}

.styles-module__controlButton___8Q0jc {
  position: relative;
  cursor: pointer !important;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.85);
  transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease, opacity 0.2s ease;
}
.styles-module__controlButton___8Q0jc:hover:not(:disabled):not([data-active=true]):not([data-failed=true]):not([data-auto-sync=true]):not([data-error=true]):not([data-no-hover=true]) {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}
.styles-module__controlButton___8Q0jc:active:not(:disabled) {
  transform: scale(0.92);
}
.styles-module__controlButton___8Q0jc:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.styles-module__controlButton___8Q0jc[data-active=true] {
  color: #3c82f7;
  background: rgba(60, 130, 247, 0.25);
}
.styles-module__controlButton___8Q0jc[data-error=true] {
  color: #ff3b30;
  background: rgba(255, 59, 48, 0.25);
}
.styles-module__controlButton___8Q0jc[data-danger]:hover:not(:disabled):not([data-active=true]):not([data-failed=true]) {
  background: rgba(255, 59, 48, 0.25);
  color: #ff3b30;
}
.styles-module__controlButton___8Q0jc[data-no-hover=true], .styles-module__controlButton___8Q0jc.styles-module__statusShowing___te6iu {
  cursor: default !important;
  pointer-events: none;
  background: transparent !important;
}
.styles-module__controlButton___8Q0jc[data-auto-sync=true] {
  color: #34c759;
  background: transparent;
  cursor: default;
}
.styles-module__controlButton___8Q0jc[data-failed=true] {
  color: #ff3b30;
  background: rgba(255, 59, 48, 0.25);
}

.styles-module__buttonBadge___NeFWb {
  position: absolute;
  top: 0px;
  right: 0px;
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  border-radius: 8px;
  background: #3c82f7;
  color: white;
  font-size: 0.625rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 0 2px #1a1a1a, 0 1px 3px rgba(0, 0, 0, 0.2);
  pointer-events: none;
}
.styles-module__buttonBadge___NeFWb.styles-module__light___r6n4Y {
  box-shadow: 0 0 0 2px #fff, 0 1px 3px rgba(0, 0, 0, 0.2);
}

@keyframes styles-module__mcpIndicatorPulseConnected___EDodZ {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0.5);
  }
  50% {
    box-shadow: 0 0 0 5px rgba(52, 199, 89, 0);
  }
}
@keyframes styles-module__mcpIndicatorPulseConnecting___cCYte {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(245, 166, 35, 0.5);
  }
  50% {
    box-shadow: 0 0 0 5px rgba(245, 166, 35, 0);
  }
}
.styles-module__mcpIndicator___zGJeL {
  position: absolute;
  top: 3px;
  right: 3px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  pointer-events: none;
  transition: background 0.3s ease, opacity 0.15s ease, transform 0.15s ease;
  opacity: 1;
  transform: scale(1);
}
.styles-module__mcpIndicator___zGJeL.styles-module__connected___7c28g {
  background: #34c759;
  animation: styles-module__mcpIndicatorPulseConnected___EDodZ 2.5s ease-in-out infinite;
}
.styles-module__mcpIndicator___zGJeL.styles-module__connecting___uo-CW {
  background: #f5a623;
  animation: styles-module__mcpIndicatorPulseConnecting___cCYte 1.5s ease-in-out infinite;
}
.styles-module__mcpIndicator___zGJeL.styles-module__hidden___Ae8H4 {
  opacity: 0;
  transform: scale(0);
  animation: none;
}

@keyframes styles-module__connectionPulse___-Zycw {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(0.9);
  }
}
.styles-module__connectionIndicatorWrapper___L-e-3 {
  width: 8px;
  height: 34px;
  margin-left: 6px;
  margin-right: 6px;
}

.styles-module__connectionIndicator___afk9p {
  position: relative;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  opacity: 0;
  transition: opacity 0.3s ease, background 0.3s ease;
  cursor: default;
}

.styles-module__connectionIndicatorVisible___C-i5B {
  opacity: 1;
}

.styles-module__connectionIndicatorConnected___IY8pR {
  background: #34c759;
  animation: styles-module__connectionPulse___-Zycw 2.5s ease-in-out infinite;
}

.styles-module__connectionIndicatorDisconnected___kmpaZ {
  background: #ff3b30;
  animation: none;
}

.styles-module__connectionIndicatorConnecting___QmSLH {
  background: #f59e0b;
  animation: styles-module__connectionPulse___-Zycw 1s ease-in-out infinite;
}

.styles-module__buttonWrapper___rBcdv {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}
.styles-module__buttonWrapper___rBcdv:hover .styles-module__buttonTooltip___Burd9 {
  opacity: 1;
  visibility: visible;
  transform: translateX(-50%) scale(1);
  transition-delay: 0.85s;
}
.styles-module__buttonWrapper___rBcdv:has(.styles-module__controlButton___8Q0jc:disabled):hover .styles-module__buttonTooltip___Burd9 {
  opacity: 0;
  visibility: hidden;
}

.styles-module__tooltipsInSession___-0lHH .styles-module__buttonWrapper___rBcdv:hover .styles-module__buttonTooltip___Burd9 {
  transition-delay: 0s;
}

.styles-module__sendButtonWrapper___UUxG6 {
  width: 0;
  opacity: 0;
  overflow: hidden;
  pointer-events: none;
  margin-left: -0.375rem;
  transition: width 0.4s cubic-bezier(0.19, 1, 0.22, 1), opacity 0.3s cubic-bezier(0.19, 1, 0.22, 1), margin 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__sendButtonWrapper___UUxG6 .styles-module__controlButton___8Q0jc {
  transform: scale(0.8);
  transition: transform 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}
.styles-module__sendButtonWrapper___UUxG6.styles-module__sendButtonVisible___WPSQU {
  width: 34px;
  opacity: 1;
  overflow: visible;
  pointer-events: auto;
  margin-left: 0;
}
.styles-module__sendButtonWrapper___UUxG6.styles-module__sendButtonVisible___WPSQU .styles-module__controlButton___8Q0jc {
  transform: scale(1);
}

.styles-module__buttonTooltip___Burd9 {
  position: absolute;
  bottom: calc(100% + 14px);
  left: 50%;
  transform: translateX(-50%) scale(0.95);
  padding: 6px 10px;
  background: #1a1a1a;
  color: rgba(255, 255, 255, 0.9);
  font-size: 12px;
  font-weight: 500;
  border-radius: 8px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  z-index: 100001;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  transition: opacity 0.135s ease, transform 0.135s ease, visibility 0.135s ease;
}
.styles-module__buttonTooltip___Burd9::after {
  content: "";
  position: absolute;
  top: calc(100% - 4px);
  left: 50%;
  transform: translateX(-50%) rotate(45deg);
  width: 8px;
  height: 8px;
  background: #1a1a1a;
  border-radius: 0 0 2px 0;
}

.styles-module__shortcut___lEAQk {
  margin-left: 4px;
  opacity: 0.5;
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonTooltip___Burd9 {
  bottom: auto;
  top: calc(100% + 14px);
  transform: translateX(-50%) scale(0.95);
}
.styles-module__tooltipBelow___m6ats .styles-module__buttonTooltip___Burd9::after {
  top: -4px;
  bottom: auto;
  border-radius: 2px 0 0 0;
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapper___rBcdv:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-50%) scale(1);
}

.styles-module__tooltipsHidden___VtLJG .styles-module__buttonTooltip___Burd9 {
  opacity: 0 !important;
  visibility: hidden !important;
  transition: none !important;
}

.styles-module__tooltipVisible___0jcCv,
.styles-module__tooltipsHidden___VtLJG .styles-module__tooltipVisible___0jcCv {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateX(-50%) scale(1) !important;
  transition-delay: 0s !important;
}

.styles-module__buttonWrapperAlignLeft___myzIp .styles-module__buttonTooltip___Burd9 {
  left: 50%;
  transform: translateX(-12px) scale(0.95);
}
.styles-module__buttonWrapperAlignLeft___myzIp .styles-module__buttonTooltip___Burd9::after {
  left: 16px;
}
.styles-module__buttonWrapperAlignLeft___myzIp:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-12px) scale(1);
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignLeft___myzIp .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-12px) scale(0.95);
}
.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignLeft___myzIp:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(-12px) scale(1);
}

.styles-module__buttonWrapperAlignRight___HCQFR .styles-module__buttonTooltip___Burd9 {
  left: 50%;
  transform: translateX(calc(-100% + 12px)) scale(0.95);
}
.styles-module__buttonWrapperAlignRight___HCQFR .styles-module__buttonTooltip___Burd9::after {
  left: auto;
  right: 8px;
}
.styles-module__buttonWrapperAlignRight___HCQFR:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(calc(-100% + 12px)) scale(1);
}

.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignRight___HCQFR .styles-module__buttonTooltip___Burd9 {
  transform: translateX(calc(-100% + 12px)) scale(0.95);
}
.styles-module__tooltipBelow___m6ats .styles-module__buttonWrapperAlignRight___HCQFR:hover .styles-module__buttonTooltip___Burd9 {
  transform: translateX(calc(-100% + 12px)) scale(1);
}

.styles-module__divider___c--s1 {
  width: 1px;
  height: 12px;
  background: rgba(255, 255, 255, 0.15);
  margin: 0 0.125rem;
}

.styles-module__overlay___Q1O9y {
  position: fixed;
  inset: 0;
  z-index: 99997;
  pointer-events: none;
}
.styles-module__overlay___Q1O9y > * {
  pointer-events: auto;
}

.styles-module__hoverHighlight___ogakW {
  position: fixed;
  border: 2px solid rgba(60, 130, 247, 0.5);
  border-radius: 4px;
  pointer-events: none !important;
  background: rgba(60, 130, 247, 0.04);
  box-sizing: border-box;
  will-change: opacity;
  contain: layout style;
}
.styles-module__hoverHighlight___ogakW.styles-module__enter___WFIki {
  animation: styles-module__hoverHighlightIn___6WYHY 0.12s ease-out forwards;
}

.styles-module__multiSelectOutline___cSJ-m {
  position: fixed;
  border: 2px dashed rgba(52, 199, 89, 0.6);
  border-radius: 4px;
  pointer-events: none !important;
  background: rgba(52, 199, 89, 0.05);
  box-sizing: border-box;
  will-change: opacity;
}
.styles-module__multiSelectOutline___cSJ-m.styles-module__enter___WFIki {
  animation: styles-module__fadeIn___b9qmf 0.15s ease-out forwards;
}
.styles-module__multiSelectOutline___cSJ-m.styles-module__exit___fyOJ0 {
  animation: styles-module__fadeOut___6Ut6- 0.15s ease-out forwards;
}

.styles-module__singleSelectOutline___QhX-O {
  position: fixed;
  border: 2px solid rgba(60, 130, 247, 0.6);
  border-radius: 4px;
  pointer-events: none !important;
  background: rgba(60, 130, 247, 0.05);
  box-sizing: border-box;
  will-change: opacity;
}
.styles-module__singleSelectOutline___QhX-O.styles-module__enter___WFIki {
  animation: styles-module__fadeIn___b9qmf 0.15s ease-out forwards;
}
.styles-module__singleSelectOutline___QhX-O.styles-module__exit___fyOJ0 {
  animation: styles-module__fadeOut___6Ut6- 0.15s ease-out forwards;
}

.styles-module__hoverTooltip___bvLk7 {
  position: fixed;
  font-size: 0.6875rem;
  font-weight: 500;
  color: #fff;
  background: rgba(0, 0, 0, 0.85);
  padding: 0.35rem 0.6rem;
  border-radius: 0.375rem;
  pointer-events: none !important;
  white-space: nowrap;
  max-width: 280px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.styles-module__hoverTooltip___bvLk7.styles-module__enter___WFIki {
  animation: styles-module__hoverTooltipIn___FYGQx 0.1s ease-out forwards;
}

.styles-module__hoverReactPath___gx1IJ {
  font-size: 0.625rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.15rem;
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__hoverElementName___QMLMl {
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__markersLayer___-25j1 {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 0;
  z-index: 99998;
  pointer-events: none;
}
.styles-module__markersLayer___-25j1 > * {
  pointer-events: auto;
}

.styles-module__fixedMarkersLayer___ffyX6 {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99998;
  pointer-events: none;
}
.styles-module__fixedMarkersLayer___ffyX6 > * {
  pointer-events: auto;
}

.styles-module__marker___6sQrs {
  position: absolute;
  width: 22px;
  height: 22px;
  background: #3c82f7;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.6875rem;
  font-weight: 600;
  transform: translate(-50%, -50%) scale(1);
  opacity: 1;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2), inset 0 0 0 1px rgba(0, 0, 0, 0.04);
  user-select: none;
  will-change: transform, opacity;
  contain: layout style;
  z-index: 1;
}
.styles-module__marker___6sQrs:hover {
  z-index: 2;
}
.styles-module__marker___6sQrs:not(.styles-module__enter___WFIki):not(.styles-module__exit___fyOJ0):not(.styles-module__clearing___FQ--7) {
  transition: background-color 0.15s ease, transform 0.1s ease;
}
.styles-module__marker___6sQrs.styles-module__enter___WFIki {
  animation: styles-module__markerIn___5FaAP 0.25s cubic-bezier(0.22, 1, 0.36, 1) both;
}
.styles-module__marker___6sQrs.styles-module__exit___fyOJ0 {
  animation: styles-module__markerOut___GU5jX 0.2s ease-out both;
  pointer-events: none;
}
.styles-module__marker___6sQrs.styles-module__clearing___FQ--7 {
  animation: styles-module__markerOut___GU5jX 0.15s ease-out both;
  pointer-events: none;
}
.styles-module__marker___6sQrs:not(.styles-module__enter___WFIki):not(.styles-module__exit___fyOJ0):not(.styles-module__clearing___FQ--7):hover {
  transform: translate(-50%, -50%) scale(1.1);
}
.styles-module__marker___6sQrs.styles-module__pending___2IHLC {
  position: fixed;
  background: #3c82f7;
}
.styles-module__marker___6sQrs.styles-module__fixed___dBMHC {
  position: fixed;
}
.styles-module__marker___6sQrs.styles-module__multiSelect___YWiuz {
  background: #34c759;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  font-size: 0.75rem;
}
.styles-module__marker___6sQrs.styles-module__multiSelect___YWiuz.styles-module__pending___2IHLC {
  background: #34c759;
}
.styles-module__marker___6sQrs.styles-module__hovered___ZgXIy {
  background: #ff3b30;
}

.styles-module__renumber___nCTxD {
  display: block;
  animation: styles-module__renumberRoll___Wgbq3 0.2s ease-out;
}

@keyframes styles-module__renumberRoll___Wgbq3 {
  0% {
    transform: translateX(-40%);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}
.styles-module__markerTooltip___aLJID {
  position: absolute;
  top: calc(100% + 10px);
  left: 50%;
  transform: translateX(-50%) scale(0.909);
  z-index: 100002;
  background: #1a1a1a;
  padding: 8px 0.75rem;
  border-radius: 0.75rem;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-weight: 400;
  color: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
  min-width: 120px;
  max-width: 200px;
  pointer-events: none;
  cursor: default;
}
.styles-module__markerTooltip___aLJID.styles-module__enter___WFIki {
  animation: styles-module__tooltipIn___0N31w 0.1s ease-out forwards;
}

.styles-module__markerQuote___FHmrz {
  display: block;
  font-size: 12px;
  font-style: italic;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 0.3125rem;
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.styles-module__markerNote___QkrrS {
  display: block;
  font-size: 13px;
  font-weight: 400;
  line-height: 1.4;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-bottom: 2px;
}

.styles-module__markerHint___2iF-6 {
  display: block;
  font-size: 0.625rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.6);
  margin-top: 0.375rem;
  white-space: nowrap;
}

.styles-module__settingsPanel___OxX3Y {
  position: absolute;
  right: 5px;
  bottom: calc(100% + 0.5rem);
  z-index: 1;
  overflow: hidden;
  background: #1c1c1c;
  border-radius: 1rem;
  padding: 13px 0 16px;
  min-width: 205px;
  cursor: default;
  opacity: 1;
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: background 0.25s ease, box-shadow 0.25s ease;
}
.styles-module__settingsPanel___OxX3Y::before, .styles-module__settingsPanel___OxX3Y::after {
  content: "";
  position: absolute;
  top: 0;
  bottom: 0;
  width: 16px;
  z-index: 2;
  pointer-events: none;
}
.styles-module__settingsPanel___OxX3Y::before {
  left: 0;
  background: linear-gradient(to right, #1c1c1c 0%, transparent 100%);
}
.styles-module__settingsPanel___OxX3Y::after {
  right: 0;
  background: linear-gradient(to left, #1c1c1c 0%, transparent 100%);
}
.styles-module__settingsPanel___OxX3Y .styles-module__settingsHeader___pwDY9,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsBrand___0gJeM,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsBrandSlash___uTG18,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsVersion___TUcFq,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsSection___m-YM2,
.styles-module__settingsPanel___OxX3Y .styles-module__settingsLabel___8UjfX,
.styles-module__settingsPanel___OxX3Y .styles-module__cycleButton___FMKfw,
.styles-module__settingsPanel___OxX3Y .styles-module__cycleDot___nPgLY,
.styles-module__settingsPanel___OxX3Y .styles-module__dropdownButton___16NPz,
.styles-module__settingsPanel___OxX3Y .styles-module__toggleLabel___Xm8Aa,
.styles-module__settingsPanel___OxX3Y .styles-module__customCheckbox___U39ax,
.styles-module__settingsPanel___OxX3Y .styles-module__sliderLabel___U8sPr,
.styles-module__settingsPanel___OxX3Y .styles-module__slider___GLdxp,
.styles-module__settingsPanel___OxX3Y .styles-module__helpIcon___xQg56,
.styles-module__settingsPanel___OxX3Y .styles-module__themeToggle___2rUjA {
  transition: background 0.25s ease, color 0.25s ease, border-color 0.25s ease;
}
.styles-module__settingsPanel___OxX3Y.styles-module__enter___WFIki {
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0px);
  transition: opacity 0.2s ease, transform 0.2s ease, filter 0.2s ease;
}
.styles-module__settingsPanel___OxX3Y.styles-module__exit___fyOJ0 {
  opacity: 0;
  transform: translateY(8px) scale(0.95);
  filter: blur(5px);
  pointer-events: none;
  transition: opacity 0.1s ease, transform 0.1s ease, filter 0.1s ease;
}
.styles-module__settingsPanel___OxX3Y.styles-module__dark___ILIQf {
  background: #1a1a1a;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.08);
}
.styles-module__settingsPanel___OxX3Y.styles-module__dark___ILIQf .styles-module__settingsLabel___8UjfX {
  color: rgba(255, 255, 255, 0.6);
}
.styles-module__settingsPanel___OxX3Y.styles-module__dark___ILIQf .styles-module__settingsOption___UNa12 {
  color: rgba(255, 255, 255, 0.85);
}
.styles-module__settingsPanel___OxX3Y.styles-module__dark___ILIQf .styles-module__settingsOption___UNa12:hover {
  background: rgba(255, 255, 255, 0.1);
}
.styles-module__settingsPanel___OxX3Y.styles-module__dark___ILIQf .styles-module__settingsOption___UNa12.styles-module__selected___OwRqP {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
}
.styles-module__settingsPanel___OxX3Y.styles-module__dark___ILIQf .styles-module__toggleLabel___Xm8Aa {
  color: rgba(255, 255, 255, 0.85);
}

.styles-module__settingsPanelContainer___Xksv8 {
  overflow: visible;
  position: relative;
  display: flex;
  padding: 0 1rem;
}
.styles-module__settingsPanelContainer___Xksv8.styles-module__transitioning___qxzCk {
  overflow-x: clip;
  overflow-y: visible;
}

.styles-module__settingsPage___6YfHH {
  min-width: 100%;
  flex-shrink: 0;
  transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1), opacity 0.2s ease-out;
  opacity: 1;
}

.styles-module__settingsPage___6YfHH.styles-module__slideLeft___Ps01J {
  transform: translateX(-100%);
  opacity: 0;
}

.styles-module__automationsPage___uvCq6 {
  position: absolute;
  top: 0;
  left: 100%;
  width: 100%;
  height: 100%;
  padding: 3px 1rem 0;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  transition: transform 0.35s cubic-bezier(0.32, 0.72, 0, 1), opacity 0.25s ease-out 0.1s;
  opacity: 0;
}

.styles-module__automationsPage___uvCq6.styles-module__slideIn___4-qXe {
  transform: translateX(-100%);
  opacity: 1;
}

.styles-module__settingsNavLink___wCzJt {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0;
  border: none;
  background: transparent;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: color 0.15s ease;
}
.styles-module__settingsNavLink___wCzJt:hover {
  color: rgba(255, 255, 255, 0.9);
}
.styles-module__settingsNavLink___wCzJt.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__settingsNavLink___wCzJt.styles-module__light___r6n4Y:hover {
  color: rgba(0, 0, 0, 0.8);
}
.styles-module__settingsNavLink___wCzJt svg {
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.15s ease;
}
.styles-module__settingsNavLink___wCzJt:hover svg {
  color: #fff;
}
.styles-module__settingsNavLink___wCzJt.styles-module__light___r6n4Y svg {
  color: rgba(0, 0, 0, 0.25);
}
.styles-module__settingsNavLink___wCzJt.styles-module__light___r6n4Y:hover svg {
  color: rgba(0, 0, 0, 0.8);
}

.styles-module__settingsNavLinkRight___ZWwhj {
  display: flex;
  align-items: center;
  gap: 6px;
}

.styles-module__mcpNavIndicator___cl9pO {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.styles-module__mcpNavIndicator___cl9pO.styles-module__connected___7c28g {
  background: #34c759;
  animation: styles-module__mcpPulse___uNggr 2.5s ease-in-out infinite;
}
.styles-module__mcpNavIndicator___cl9pO.styles-module__connecting___uo-CW {
  background: #f5a623;
  animation: styles-module__mcpPulse___uNggr 1.5s ease-in-out infinite;
}

.styles-module__settingsBackButton___bIe2j {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 0 12px 0;
  margin: -6px 0 0.5rem 0;
  border: none;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 0;
  background: transparent;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 500;
  letter-spacing: -0.15px;
  color: #fff;
  cursor: pointer;
  transition: transform 0.12s cubic-bezier(0.32, 0.72, 0, 1);
}
.styles-module__settingsBackButton___bIe2j svg {
  opacity: 0.4;
  flex-shrink: 0;
  transition: opacity 0.15s ease, transform 0.18s cubic-bezier(0.32, 0.72, 0, 1);
}
.styles-module__settingsBackButton___bIe2j:hover {
  border-bottom-color: rgba(255, 255, 255, 0.07);
}
.styles-module__settingsBackButton___bIe2j:hover svg {
  opacity: 1;
}
.styles-module__settingsBackButton___bIe2j.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.85);
  border-bottom-color: rgba(0, 0, 0, 0.08);
}
.styles-module__settingsBackButton___bIe2j.styles-module__light___r6n4Y:hover {
  border-bottom-color: rgba(0, 0, 0, 0.08);
}

.styles-module__automationHeader___InP0r {
  display: flex;
  align-items: center;
  gap: 0.125rem;
  font-size: 0.8125rem;
  font-weight: 400;
  color: #fff;
}
.styles-module__automationHeader___InP0r .styles-module__helpIcon___xQg56 svg {
  transform: none;
}
.styles-module__automationHeader___InP0r.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__automationDescription___NKlmo {
  font-size: 0.6875rem;
  font-weight: 300;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 2px;
  line-height: 14px;
}
.styles-module__automationDescription___NKlmo.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__learnMoreLink___8xv-x {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: underline dotted;
  text-decoration-color: rgba(255, 255, 255, 0.2);
  text-underline-offset: 2px;
  transition: color 0.15s ease;
}
.styles-module__learnMoreLink___8xv-x:hover {
  color: #fff;
}
.styles-module__learnMoreLink___8xv-x.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.6);
  text-decoration-color: rgba(0, 0, 0, 0.2);
}
.styles-module__learnMoreLink___8xv-x.styles-module__light___r6n4Y:hover {
  color: rgba(0, 0, 0, 0.85);
}

.styles-module__autoSendRow___UblX5 {
  display: flex;
  align-items: center;
  gap: 8px;
}

.styles-module__autoSendLabel___icDc2 {
  font-size: 0.6875rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.15s ease;
}
.styles-module__autoSendLabel___icDc2.styles-module__active___-zoN6 {
  color: #66b8ff;
}
.styles-module__autoSendLabel___icDc2.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__autoSendLabel___icDc2.styles-module__light___r6n4Y.styles-module__active___-zoN6 {
  color: #3c82f7;
}

.styles-module__webhookUrlInput___2375C {
  display: block;
  width: 100%;
  flex: 1;
  min-height: 60px;
  box-sizing: border-box;
  margin-top: 11px;
  padding: 8px 10px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.03);
  font-family: inherit;
  font-size: 0.75rem;
  font-weight: 400;
  color: #fff;
  outline: none;
  resize: none;
  cursor: text !important;
  user-select: text;
  transition: border-color 0.15s ease, background 0.15s ease, box-shadow 0.15s ease;
}
.styles-module__webhookUrlInput___2375C::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
.styles-module__webhookUrlInput___2375C:focus {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.08);
}
.styles-module__webhookUrlInput___2375C.styles-module__light___r6n4Y {
  border-color: rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.03);
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__webhookUrlInput___2375C.styles-module__light___r6n4Y::placeholder {
  color: rgba(0, 0, 0, 0.3);
}
.styles-module__webhookUrlInput___2375C.styles-module__light___r6n4Y:focus {
  border-color: rgba(0, 0, 0, 0.25);
  background: rgba(0, 0, 0, 0.05);
}

.styles-module__settingsHeader___pwDY9 {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 24px;
  margin-bottom: 0.5rem;
  padding-bottom: 9px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.styles-module__settingsBrand___0gJeM {
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: -0.0094em;
  color: #fff;
}

.styles-module__settingsBrandSlash___uTG18 {
  color: rgba(255, 255, 255, 0.5);
}

.styles-module__settingsVersion___TUcFq {
  font-size: 11px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.4);
  margin-left: auto;
  letter-spacing: -0.0094em;
}

.styles-module__settingsSection___m-YM2 + .styles-module__settingsSection___m-YM2 {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.07);
}
.styles-module__settingsSection___m-YM2.styles-module__settingsSectionExtraPadding___jdhFV {
  padding-top: calc(0.5rem + 4px);
}

.styles-module__settingsSectionGrow___h-5HZ {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.styles-module__settingsRow___3sdhc {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 24px;
}
.styles-module__settingsRow___3sdhc.styles-module__settingsRowMarginTop___zA0Sp {
  margin-top: 8px;
}

.styles-module__dropdownContainer___BVnxe {
  position: relative;
}

.styles-module__dropdownButton___16NPz {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.5rem;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  font-size: 0.8125rem;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
  letter-spacing: -0.0094em;
}
.styles-module__dropdownButton___16NPz:hover {
  background: rgba(255, 255, 255, 0.08);
}
.styles-module__dropdownButton___16NPz svg {
  opacity: 0.6;
}

.styles-module__cycleButton___FMKfw {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0;
  border: none;
  background: transparent;
  font-size: 0.8125rem;
  font-weight: 500;
  color: #fff;
  cursor: pointer;
  letter-spacing: -0.0094em;
}
.styles-module__cycleButton___FMKfw.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__cycleButton___FMKfw:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.styles-module__settingsRowDisabled___EgS0V .styles-module__settingsLabel___8UjfX {
  color: rgba(255, 255, 255, 0.2);
}
.styles-module__settingsRowDisabled___EgS0V .styles-module__settingsLabel___8UjfX.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.2);
}
.styles-module__settingsRowDisabled___EgS0V .styles-module__toggleSwitch___l4Ygm {
  opacity: 0.4;
  cursor: not-allowed;
}

@keyframes styles-module__cycleTextIn___Q6zJf {
  0% {
    opacity: 0;
    transform: translateY(-6px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
.styles-module__cycleButtonText___fD1LR {
  display: inline-block;
  animation: styles-module__cycleTextIn___Q6zJf 0.2s ease-out;
}

.styles-module__cycleDots___LWuoQ {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.styles-module__cycleDot___nPgLY {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0.667);
  transition: background-color 0.25s ease-out, transform 0.25s ease-out;
}
.styles-module__cycleDot___nPgLY.styles-module__active___-zoN6 {
  background: #fff;
  transform: scale(1);
}
.styles-module__cycleDot___nPgLY.styles-module__light___r6n4Y {
  background: rgba(0, 0, 0, 0.2);
}
.styles-module__cycleDot___nPgLY.styles-module__light___r6n4Y.styles-module__active___-zoN6 {
  background: rgba(0, 0, 0, 0.7);
}

.styles-module__dropdownMenu___k73ER {
  position: absolute;
  right: 0;
  top: calc(100% + 0.25rem);
  background: #1a1a1a;
  border-radius: 0.5rem;
  padding: 0.25rem;
  min-width: 120px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.1);
  z-index: 10;
  animation: styles-module__scaleIn___c-r1K 0.15s ease-out;
}

.styles-module__dropdownItem___ylsLj {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0.5rem 0.625rem;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  font-size: 0.8125rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.85);
  cursor: pointer;
  text-align: left;
  transition: background-color 0.15s ease, color 0.15s ease;
  letter-spacing: -0.0094em;
}
.styles-module__dropdownItem___ylsLj:hover {
  background: rgba(255, 255, 255, 0.08);
}
.styles-module__dropdownItem___ylsLj.styles-module__selected___OwRqP {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
  font-weight: 600;
}

.styles-module__settingsLabel___8UjfX {
  font-size: 0.8125rem;
  font-weight: 400;
  letter-spacing: -0.0094em;
  color: rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  gap: 0.125rem;
}
.styles-module__settingsLabel___8UjfX.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__settingsLabelMarker___ewdtV {
  padding-top: 3px;
  margin-bottom: 10px;
}

.styles-module__settingsOptions___LyrBA {
  display: flex;
  gap: 0.25rem;
}

.styles-module__settingsOption___UNa12 {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.375rem 0.5rem;
  border: none;
  border-radius: 0.375rem;
  background: transparent;
  font-size: 0.6875rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.7);
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}
.styles-module__settingsOption___UNa12:hover {
  background: rgba(0, 0, 0, 0.05);
}
.styles-module__settingsOption___UNa12.styles-module__selected___OwRqP {
  background: rgba(60, 130, 247, 0.15);
  color: #3c82f7;
}

.styles-module__sliderContainer___ducXj {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.styles-module__slider___GLdxp {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 2px;
  outline: none;
  cursor: pointer;
}
.styles-module__slider___GLdxp::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 14px;
  height: 14px;
  background: white;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}
.styles-module__slider___GLdxp::-moz-range-thumb {
  width: 14px;
  height: 14px;
  background: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
}
.styles-module__slider___GLdxp:hover::-webkit-slider-thumb {
  transform: scale(1.15);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}
.styles-module__slider___GLdxp:hover::-moz-range-thumb {
  transform: scale(1.15);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}

.styles-module__sliderLabels___FhLDB {
  display: flex;
  justify-content: space-between;
}

.styles-module__sliderLabel___U8sPr {
  font-size: 0.625rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: color 0.15s ease;
}
.styles-module__sliderLabel___U8sPr:hover {
  color: rgba(255, 255, 255, 0.7);
}
.styles-module__sliderLabel___U8sPr.styles-module__active___-zoN6 {
  color: rgba(255, 255, 255, 0.9);
}

.styles-module__colorOptions___iHCNX {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.375rem;
  margin-bottom: 1px;
}

.styles-module__colorOption___IodiY {
  display: block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid transparent;
  cursor: pointer;
  transition: transform 0.2s cubic-bezier(0.25, 1, 0.5, 1);
}
.styles-module__colorOption___IodiY:hover {
  transform: scale(1.15);
}
.styles-module__colorOption___IodiY.styles-module__selected___OwRqP {
  transform: scale(0.83);
}

.styles-module__colorOptionRing___U2xpo {
  display: flex;
  width: 24px;
  height: 24px;
  border: 2px solid transparent;
  border-radius: 50%;
  transition: border-color 0.3s ease;
}
.styles-module__settingsToggle___fBrFn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}
.styles-module__settingsToggle___fBrFn + .styles-module__settingsToggle___fBrFn {
  margin-top: calc(0.5rem + 6px);
}
.styles-module__settingsToggle___fBrFn input[type=checkbox] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}
.styles-module__settingsToggle___fBrFn.styles-module__settingsToggleMarginBottom___MZUyF {
  margin-bottom: calc(0.5rem + 6px);
}

.styles-module__customCheckbox___U39ax {
  position: relative;
  width: 14px;
  height: 14px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.25s ease, border-color 0.25s ease;
}
.styles-module__customCheckbox___U39ax svg {
  color: #1a1a1a;
  opacity: 1;
  transition: opacity 0.15s ease;
}
input[type=checkbox]:checked + .styles-module__customCheckbox___U39ax {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgb(255, 255, 255);
}
.styles-module__customCheckbox___U39ax.styles-module__light___r6n4Y {
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: #fff;
}
.styles-module__customCheckbox___U39ax.styles-module__light___r6n4Y.styles-module__checked___mnZLo {
  border-color: #1a1a1a;
  background: #1a1a1a;
}
.styles-module__customCheckbox___U39ax.styles-module__light___r6n4Y.styles-module__checked___mnZLo svg {
  color: #fff;
}

.styles-module__toggleLabel___Xm8Aa {
  font-size: 0.8125rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.5);
  letter-spacing: -0.0094em;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}
.styles-module__toggleLabel___Xm8Aa.styles-module__light___r6n4Y {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__toggleSwitch___l4Ygm {
  position: relative;
  display: inline-block;
  width: 24px;
  height: 16px;
  flex-shrink: 0;
  cursor: pointer;
  transition: opacity 0.15s ease;
}
.styles-module__toggleSwitch___l4Ygm input {
  opacity: 0;
  width: 0;
  height: 0;
}
.styles-module__toggleSwitch___l4Ygm input:checked + .styles-module__toggleSlider___wprIn {
  background: #3c82f7;
}
.styles-module__toggleSwitch___l4Ygm input:checked + .styles-module__toggleSlider___wprIn::before {
  transform: translateX(8px);
}
.styles-module__toggleSwitch___l4Ygm.styles-module__disabled___332Jw {
  opacity: 0.4;
  pointer-events: none;
}
.styles-module__toggleSwitch___l4Ygm.styles-module__disabled___332Jw .styles-module__toggleSlider___wprIn {
  cursor: not-allowed;
}

.styles-module__toggleSlider___wprIn {
  position: absolute;
  cursor: pointer;
  inset: 0;
  border-radius: 16px;
  background: #484848;
}
.styles-module__light___r6n4Y .styles-module__toggleSlider___wprIn {
  background: #dddddd;
}
.styles-module__toggleSlider___wprIn::before {
  content: "";
  position: absolute;
  height: 12px;
  width: 12px;
  left: 2px;
  bottom: 2px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

@keyframes styles-module__mcpPulse___uNggr {
  0% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0.5);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(52, 199, 89, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(52, 199, 89, 0);
  }
}
@keyframes styles-module__mcpPulseError___fov9B {
  0% {
    box-shadow: 0 0 0 0 rgba(255, 59, 48, 0.5);
  }
  70% {
    box-shadow: 0 0 0 6px rgba(255, 59, 48, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(255, 59, 48, 0);
  }
}
.styles-module__mcpStatusDot___ibgkc {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
.styles-module__mcpStatusDot___ibgkc.styles-module__connecting___uo-CW {
  background: #f5a623;
  animation: styles-module__mcpPulse___uNggr 1.5s infinite;
}
.styles-module__mcpStatusDot___ibgkc.styles-module__connected___7c28g {
  background: #34c759;
  animation: styles-module__mcpPulse___uNggr 2.5s ease-in-out infinite;
}
.styles-module__mcpStatusDot___ibgkc.styles-module__disconnected___cHPxR {
  background: #ff3b30;
  animation: styles-module__mcpPulseError___fov9B 2s infinite;
}

.styles-module__helpIcon___xQg56 {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: help;
  margin-left: 0;
}
.styles-module__helpIcon___xQg56 svg {
  display: block;
  transform: translateY(1px);
  color: rgba(255, 255, 255, 0.2);
  transition: color 0.15s ease;
}
.styles-module__helpIcon___xQg56:hover svg {
  color: rgba(255, 255, 255, 0.5);
}
.styles-module__helpIcon___xQg56.styles-module__helpIconNudgeDown___0cqpM svg {
  transform: translateY(1px);
}
.styles-module__helpIcon___xQg56.styles-module__helpIconNoNudge___abogC svg {
  transform: translateY(0.5px);
}
.styles-module__helpIcon___xQg56.styles-module__helpIconNudge1-5___DM2TQ svg {
  transform: translateY(1.5px);
}
.styles-module__helpIcon___xQg56.styles-module__helpIconNudge2___TfWgC svg {
  transform: translateY(2px);
}

.styles-module__dragSelection___kZLq2 {
  position: fixed;
  top: 0;
  left: 0;
  border: 2px solid rgba(52, 199, 89, 0.6);
  border-radius: 4px;
  background: rgba(52, 199, 89, 0.08);
  pointer-events: none;
  z-index: 99997;
  will-change: transform, width, height;
  contain: layout style;
}

.styles-module__dragCount___KM90j {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #34c759;
  color: white;
  font-size: 0.875rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 1rem;
  min-width: 1.5rem;
  text-align: center;
}

.styles-module__highlightsContainer___-0xzG {
  position: fixed;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 99996;
}

.styles-module__selectedElementHighlight___fyVlI {
  position: fixed;
  top: 0;
  left: 0;
  border: 2px solid rgba(52, 199, 89, 0.5);
  border-radius: 4px;
  background: rgba(52, 199, 89, 0.06);
  pointer-events: none;
  will-change: transform, width, height;
  contain: layout style;
}

.styles-module__light___r6n4Y.styles-module__toolbarContainer___dIhma {
  background: #fff;
  color: rgba(0, 0, 0, 0.85);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
}
.styles-module__light___r6n4Y.styles-module__toolbarContainer___dIhma.styles-module__collapsed___Rydsn:hover {
  background: #f5f5f5;
}
.styles-module__light___r6n4Y.styles-module__controlButton___8Q0jc {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___r6n4Y.styles-module__controlButton___8Q0jc:hover:not(:disabled):not([data-active=true]):not([data-failed=true]):not([data-auto-sync=true]):not([data-error=true]):not([data-no-hover=true]) {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__light___r6n4Y.styles-module__controlButton___8Q0jc[data-active=true] {
  color: #3c82f7;
  background: rgba(60, 130, 247, 0.15);
}
.styles-module__light___r6n4Y.styles-module__controlButton___8Q0jc[data-error=true] {
  color: #ff3b30;
  background: rgba(255, 59, 48, 0.15);
}
.styles-module__light___r6n4Y.styles-module__controlButton___8Q0jc[data-danger]:hover:not(:disabled):not([data-active=true]):not([data-failed=true]) {
  background: rgba(255, 59, 48, 0.15);
  color: #ff3b30;
}
.styles-module__light___r6n4Y.styles-module__controlButton___8Q0jc[data-auto-sync=true] {
  color: #34c759;
  background: transparent;
}
.styles-module__light___r6n4Y.styles-module__controlButton___8Q0jc[data-failed=true] {
  color: #ff3b30;
  background: rgba(255, 59, 48, 0.15);
}
.styles-module__light___r6n4Y.styles-module__buttonTooltip___Burd9 {
  background: #fff;
  color: rgba(0, 0, 0, 0.85);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
}
.styles-module__light___r6n4Y.styles-module__buttonTooltip___Burd9::after {
  background: #fff;
}
.styles-module__light___r6n4Y.styles-module__divider___c--s1 {
  background: rgba(0, 0, 0, 0.1);
}
.styles-module__light___r6n4Y.styles-module__markerTooltip___aLJID {
  background: #fff;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(0, 0, 0, 0.06);
}
.styles-module__light___r6n4Y.styles-module__markerTooltip___aLJID .styles-module__markerQuote___FHmrz {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___r6n4Y.styles-module__markerTooltip___aLJID .styles-module__markerNote___QkrrS {
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__light___r6n4Y.styles-module__markerTooltip___aLJID .styles-module__markerHint___2iF-6 {
  color: rgba(0, 0, 0, 0.35);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08), 0 4px 16px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y::before {
  background: linear-gradient(to right, #fff 0%, transparent 100%);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y::after {
  background: linear-gradient(to left, #fff 0%, transparent 100%);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__settingsHeader___pwDY9 {
  border-bottom-color: rgba(0, 0, 0, 0.08);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__settingsBrand___0gJeM {
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__settingsBrandSlash___uTG18 {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__settingsVersion___TUcFq {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__settingsSection___m-YM2 {
  border-top-color: rgba(0, 0, 0, 0.08);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__settingsLabel___8UjfX {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__cycleButton___FMKfw {
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__cycleDot___nPgLY {
  background: rgba(0, 0, 0, 0.2);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__cycleDot___nPgLY.styles-module__active___-zoN6 {
  background: rgba(0, 0, 0, 0.7);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__dropdownButton___16NPz {
  color: rgba(0, 0, 0, 0.85);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__dropdownButton___16NPz:hover {
  background: rgba(0, 0, 0, 0.05);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__toggleLabel___Xm8Aa {
  color: rgba(0, 0, 0, 0.5);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__customCheckbox___U39ax {
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: #fff;
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__customCheckbox___U39ax.styles-module__checked___mnZLo {
  border-color: #1a1a1a;
  background: #1a1a1a;
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__customCheckbox___U39ax.styles-module__checked___mnZLo svg {
  color: #fff;
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__sliderLabel___U8sPr {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__sliderLabel___U8sPr:hover {
  color: rgba(0, 0, 0, 0.7);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__sliderLabel___U8sPr.styles-module__active___-zoN6 {
  color: rgba(0, 0, 0, 0.9);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__slider___GLdxp {
  background: rgba(0, 0, 0, 0.1);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__slider___GLdxp::-webkit-slider-thumb {
  background: #1a1a1a;
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__slider___GLdxp::-moz-range-thumb {
  background: #1a1a1a;
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__helpIcon___xQg56 svg {
  color: rgba(0, 0, 0, 0.2);
}
.styles-module__light___r6n4Y.styles-module__settingsPanel___OxX3Y .styles-module__helpIcon___xQg56:hover svg {
  color: rgba(0, 0, 0, 0.5);
}

.styles-module__themeToggle___2rUjA {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  margin-left: 0.5rem;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: background-color 0.15s ease, color 0.15s ease;
}
.styles-module__themeToggle___2rUjA:hover {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}
.styles-module__light___r6n4Y .styles-module__themeToggle___2rUjA {
  color: rgba(0, 0, 0, 0.4);
}
.styles-module__light___r6n4Y .styles-module__themeToggle___2rUjA:hover {
  background: rgba(0, 0, 0, 0.06);
  color: rgba(0, 0, 0, 0.7);
}

.styles-module__themeIconWrapper___LsJIM {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  width: 20px;
  height: 20px;
}

.styles-module__themeIcon___lCCmo {
  display: flex;
  align-items: center;
  justify-content: center;
  animation: styles-module__themeIconIn___TU6ML 0.35s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes styles-module__themeIconIn___TU6ML {
  0% {
    opacity: 0;
    transform: scale(0.8) rotate(-30deg);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
  }
}`,Ig={toolbar:"styles-module__toolbar___wNsdK",markersLayer:"styles-module__markersLayer___-25j1",fixedMarkersLayer:"styles-module__fixedMarkersLayer___ffyX6",toolbarContainer:"styles-module__toolbarContainer___dIhma",dragging:"styles-module__dragging___xrolZ",entrance:"styles-module__entrance___sgHd8",toolbarEnter:"styles-module__toolbarEnter___u8RRu",hiding:"styles-module__hiding___1td44",toolbarHide:"styles-module__toolbarHide___y8kaT",collapsed:"styles-module__collapsed___Rydsn",expanded:"styles-module__expanded___ofKPx",serverConnected:"styles-module__serverConnected___Gfbou",toggleContent:"styles-module__toggleContent___0yfyP",visible:"styles-module__visible___KHwEW",hidden:"styles-module__hidden___Ae8H4",controlsContent:"styles-module__controlsContent___9GJWU",badge:"styles-module__badge___2XsgF",fadeOut:"styles-module__fadeOut___6Ut6-",badgeEnter:"styles-module__badgeEnter___mVQLj",controlButton:"styles-module__controlButton___8Q0jc",statusShowing:"styles-module__statusShowing___te6iu",buttonBadge:"styles-module__buttonBadge___NeFWb",light:"styles-module__light___r6n4Y",mcpIndicator:"styles-module__mcpIndicator___zGJeL",connected:"styles-module__connected___7c28g",mcpIndicatorPulseConnected:"styles-module__mcpIndicatorPulseConnected___EDodZ",connecting:"styles-module__connecting___uo-CW",mcpIndicatorPulseConnecting:"styles-module__mcpIndicatorPulseConnecting___cCYte",connectionIndicatorWrapper:"styles-module__connectionIndicatorWrapper___L-e-3",connectionIndicator:"styles-module__connectionIndicator___afk9p",connectionIndicatorVisible:"styles-module__connectionIndicatorVisible___C-i5B",connectionIndicatorConnected:"styles-module__connectionIndicatorConnected___IY8pR",connectionPulse:"styles-module__connectionPulse___-Zycw",connectionIndicatorDisconnected:"styles-module__connectionIndicatorDisconnected___kmpaZ",connectionIndicatorConnecting:"styles-module__connectionIndicatorConnecting___QmSLH",buttonWrapper:"styles-module__buttonWrapper___rBcdv",buttonTooltip:"styles-module__buttonTooltip___Burd9",tooltipsInSession:"styles-module__tooltipsInSession___-0lHH",sendButtonWrapper:"styles-module__sendButtonWrapper___UUxG6",sendButtonVisible:"styles-module__sendButtonVisible___WPSQU",shortcut:"styles-module__shortcut___lEAQk",tooltipBelow:"styles-module__tooltipBelow___m6ats",tooltipsHidden:"styles-module__tooltipsHidden___VtLJG",tooltipVisible:"styles-module__tooltipVisible___0jcCv",buttonWrapperAlignLeft:"styles-module__buttonWrapperAlignLeft___myzIp",buttonWrapperAlignRight:"styles-module__buttonWrapperAlignRight___HCQFR",divider:"styles-module__divider___c--s1",overlay:"styles-module__overlay___Q1O9y",hoverHighlight:"styles-module__hoverHighlight___ogakW",enter:"styles-module__enter___WFIki",hoverHighlightIn:"styles-module__hoverHighlightIn___6WYHY",multiSelectOutline:"styles-module__multiSelectOutline___cSJ-m",fadeIn:"styles-module__fadeIn___b9qmf",exit:"styles-module__exit___fyOJ0",singleSelectOutline:"styles-module__singleSelectOutline___QhX-O",hoverTooltip:"styles-module__hoverTooltip___bvLk7",hoverTooltipIn:"styles-module__hoverTooltipIn___FYGQx",hoverReactPath:"styles-module__hoverReactPath___gx1IJ",hoverElementName:"styles-module__hoverElementName___QMLMl",marker:"styles-module__marker___6sQrs",clearing:"styles-module__clearing___FQ--7",markerIn:"styles-module__markerIn___5FaAP",markerOut:"styles-module__markerOut___GU5jX",pending:"styles-module__pending___2IHLC",fixed:"styles-module__fixed___dBMHC",multiSelect:"styles-module__multiSelect___YWiuz",hovered:"styles-module__hovered___ZgXIy",renumber:"styles-module__renumber___nCTxD",renumberRoll:"styles-module__renumberRoll___Wgbq3",markerTooltip:"styles-module__markerTooltip___aLJID",tooltipIn:"styles-module__tooltipIn___0N31w",markerQuote:"styles-module__markerQuote___FHmrz",markerNote:"styles-module__markerNote___QkrrS",markerHint:"styles-module__markerHint___2iF-6",settingsPanel:"styles-module__settingsPanel___OxX3Y",settingsHeader:"styles-module__settingsHeader___pwDY9",settingsBrand:"styles-module__settingsBrand___0gJeM",settingsBrandSlash:"styles-module__settingsBrandSlash___uTG18",settingsVersion:"styles-module__settingsVersion___TUcFq",settingsSection:"styles-module__settingsSection___m-YM2",settingsLabel:"styles-module__settingsLabel___8UjfX",cycleButton:"styles-module__cycleButton___FMKfw",cycleDot:"styles-module__cycleDot___nPgLY",dropdownButton:"styles-module__dropdownButton___16NPz",toggleLabel:"styles-module__toggleLabel___Xm8Aa",customCheckbox:"styles-module__customCheckbox___U39ax",sliderLabel:"styles-module__sliderLabel___U8sPr",slider:"styles-module__slider___GLdxp",helpIcon:"styles-module__helpIcon___xQg56",themeToggle:"styles-module__themeToggle___2rUjA",dark:"styles-module__dark___ILIQf",settingsOption:"styles-module__settingsOption___UNa12",selected:"styles-module__selected___OwRqP",settingsPanelContainer:"styles-module__settingsPanelContainer___Xksv8",transitioning:"styles-module__transitioning___qxzCk",settingsPage:"styles-module__settingsPage___6YfHH",slideLeft:"styles-module__slideLeft___Ps01J",automationsPage:"styles-module__automationsPage___uvCq6",slideIn:"styles-module__slideIn___4-qXe",settingsNavLink:"styles-module__settingsNavLink___wCzJt",settingsNavLinkRight:"styles-module__settingsNavLinkRight___ZWwhj",mcpNavIndicator:"styles-module__mcpNavIndicator___cl9pO",mcpPulse:"styles-module__mcpPulse___uNggr",settingsBackButton:"styles-module__settingsBackButton___bIe2j",automationHeader:"styles-module__automationHeader___InP0r",automationDescription:"styles-module__automationDescription___NKlmo",learnMoreLink:"styles-module__learnMoreLink___8xv-x",autoSendRow:"styles-module__autoSendRow___UblX5",autoSendLabel:"styles-module__autoSendLabel___icDc2",active:"styles-module__active___-zoN6",webhookUrlInput:"styles-module__webhookUrlInput___2375C",settingsSectionExtraPadding:"styles-module__settingsSectionExtraPadding___jdhFV",settingsSectionGrow:"styles-module__settingsSectionGrow___h-5HZ",settingsRow:"styles-module__settingsRow___3sdhc",settingsRowMarginTop:"styles-module__settingsRowMarginTop___zA0Sp",dropdownContainer:"styles-module__dropdownContainer___BVnxe",settingsRowDisabled:"styles-module__settingsRowDisabled___EgS0V",toggleSwitch:"styles-module__toggleSwitch___l4Ygm",cycleButtonText:"styles-module__cycleButtonText___fD1LR",cycleTextIn:"styles-module__cycleTextIn___Q6zJf",cycleDots:"styles-module__cycleDots___LWuoQ",dropdownMenu:"styles-module__dropdownMenu___k73ER",scaleIn:"styles-module__scaleIn___c-r1K",dropdownItem:"styles-module__dropdownItem___ylsLj",settingsLabelMarker:"styles-module__settingsLabelMarker___ewdtV",settingsOptions:"styles-module__settingsOptions___LyrBA",sliderContainer:"styles-module__sliderContainer___ducXj",sliderLabels:"styles-module__sliderLabels___FhLDB",colorOptions:"styles-module__colorOptions___iHCNX",colorOption:"styles-module__colorOption___IodiY",colorOptionRing:"styles-module__colorOptionRing___U2xpo",settingsToggle:"styles-module__settingsToggle___fBrFn",settingsToggleMarginBottom:"styles-module__settingsToggleMarginBottom___MZUyF",checked:"styles-module__checked___mnZLo",toggleSlider:"styles-module__toggleSlider___wprIn",disabled:"styles-module__disabled___332Jw",mcpStatusDot:"styles-module__mcpStatusDot___ibgkc",disconnected:"styles-module__disconnected___cHPxR",mcpPulseError:"styles-module__mcpPulseError___fov9B",helpIconNudgeDown:"styles-module__helpIconNudgeDown___0cqpM",helpIconNoNudge:"styles-module__helpIconNoNudge___abogC","helpIconNudge1-5":"styles-module__helpIconNudge1-5___DM2TQ",helpIconNudge2:"styles-module__helpIconNudge2___TfWgC",dragSelection:"styles-module__dragSelection___kZLq2",dragCount:"styles-module__dragCount___KM90j",highlightsContainer:"styles-module__highlightsContainer___-0xzG",selectedElementHighlight:"styles-module__selectedElementHighlight___fyVlI",themeIconWrapper:"styles-module__themeIconWrapper___LsJIM",themeIcon:"styles-module__themeIcon___lCCmo",themeIconIn:"styles-module__themeIconIn___TU6ML",scaleOut:"styles-module__scaleOut___Wctwz",slideUp:"styles-module__slideUp___kgD36",slideDown:"styles-module__slideDown___zcdje",settingsPanelIn:"styles-module__settingsPanelIn___MGfO8",settingsPanelOut:"styles-module__settingsPanelOut___Zfymi"};if(typeof document<"u"){let e=document.getElementById("feedback-tool-styles-page-toolbar-css-styles");e||(e=document.createElement("style"),e.id="feedback-tool-styles-page-toolbar-css-styles",e.textContent=Wg,document.head.appendChild(e))}var r=Ig;function bd(e,t="filtered"){let{name:n,path:l}=iu(e);if(t==="off")return{name:n,elementName:n,path:l,reactComponents:null};let a=Rg(e,{mode:t});return{name:a.path?`${a.path} ${n}`:n,elementName:n,path:l,reactComponents:a.path}}var h5=!1,y5={outputDetail:"standard",autoClearAfterCopy:!1,annotationColor:"#3c82f7",blockInteractions:!0,reactEnabled:!0,markerClickBehavior:"edit",webhookUrl:"",webhooksEnabled:!0},an=e=>{if(!e||!e.trim())return!1;try{let t=new URL(e.trim());return t.protocol==="http:"||t.protocol==="https:"}catch{return!1}},Fg={compact:"off",standard:"filtered",detailed:"smart",forensic:"all"},si=[{value:"compact",label:"Compact"},{value:"standard",label:"Standard"},{value:"detailed",label:"Detailed"},{value:"forensic",label:"Forensic"}],Pg=[{value:"#AF52DE",label:"Purple"},{value:"#3c82f7",label:"Blue"},{value:"#5AC8FA",label:"Cyan"},{value:"#34C759",label:"Green"},{value:"#FFD60A",label:"Yellow"},{value:"#FF9500",label:"Orange"},{value:"#FF3B30",label:"Red"}];function $a(e,t){let n=document.elementFromPoint(e,t);if(!n)return null;for(;n?.shadowRoot;){let l=n.shadowRoot.elementFromPoint(e,t);if(!l||l===n)break;n=l}return n}function vd(e){let t=e;for(;t&&t!==document.body;){let l=window.getComputedStyle(t).position;if(l==="fixed"||l==="sticky")return!0;t=t.parentElement}return!1}function _l(e){return e.status!=="resolved"&&e.status!=="dismissed"}function ou(e){let t=Ed(e),n=t.found?t:Jg(e);if(n.found&&n.source)return Kg(n.source,"path")}function g5(e,t,n="standard",l="filtered"){if(e.length===0)return"";let a=typeof window<"u"?`${window.innerWidth}\xD7${window.innerHeight}`:"unknown",o=`## Page Feedback: ${t}
`;return n==="forensic"?(o+=`
**Environment:**
`,o+=`- Viewport: ${a}
`,typeof window<"u"&&(o+=`- URL: ${window.location.href}
`,o+=`- User Agent: ${navigator.userAgent}
`,o+=`- Timestamp: ${new Date().toISOString()}
`,o+=`- Device Pixel Ratio: ${window.devicePixelRatio}
`),o+=`
---
`):n!=="compact"&&(o+=`**Viewport:** ${a}
`),o+=`
`,e.forEach((i,s)=>{n==="compact"?(o+=`${s+1}. **${i.element}**${i.sourceFile?` (${i.sourceFile})`:""}: ${i.comment}`,i.selectedText&&(o+=` (re: "${i.selectedText.slice(0,30)}${i.selectedText.length>30?"...":""}")`),o+=`
`):n==="forensic"?(o+=`### ${s+1}. ${i.element}
`,i.isMultiSelect&&i.fullPath&&(o+=`*Forensic data shown for first element of selection*
`),i.fullPath&&(o+=`**Full DOM Path:** ${i.fullPath}
`),i.cssClasses&&(o+=`**CSS Classes:** ${i.cssClasses}
`),i.boundingBox&&(o+=`**Position:** x:${Math.round(i.boundingBox.x)}, y:${Math.round(i.boundingBox.y)} (${Math.round(i.boundingBox.width)}\xD7${Math.round(i.boundingBox.height)}px)
`),o+=`**Annotation at:** ${i.x.toFixed(1)}% from left, ${Math.round(i.y)}px from top
`,i.selectedText&&(o+=`**Selected text:** "${i.selectedText}"
`),i.nearbyText&&!i.selectedText&&(o+=`**Context:** ${i.nearbyText.slice(0,100)}
`),i.computedStyles&&(o+=`**Computed Styles:** ${i.computedStyles}
`),i.accessibility&&(o+=`**Accessibility:** ${i.accessibility}
`),i.nearbyElements&&(o+=`**Nearby Elements:** ${i.nearbyElements}
`),i.sourceFile&&(o+=`**Source:** ${i.sourceFile}
`),i.reactComponents&&(o+=`**React:** ${i.reactComponents}
`),o+=`**Feedback:** ${i.comment}

`):(o+=`### ${s+1}. ${i.element}
`,o+=`**Location:** ${i.elementPath}
`,i.sourceFile&&(o+=`**Source:** ${i.sourceFile}
`),i.reactComponents&&(o+=`**React:** ${i.reactComponents}
`),n==="detailed"&&(i.cssClasses&&(o+=`**Classes:** ${i.cssClasses}
`),i.boundingBox&&(o+=`**Position:** ${Math.round(i.boundingBox.x)}px, ${Math.round(i.boundingBox.y)}px (${Math.round(i.boundingBox.width)}\xD7${Math.round(i.boundingBox.height)}px)
`)),i.selectedText&&(o+=`**Selected text:** "${i.selectedText}"
`),n==="detailed"&&i.nearbyText&&!i.selectedText&&(o+=`**Context:** ${i.nearbyText.slice(0,100)}
`),o+=`**Feedback:** ${i.comment}

`)}),o.trim()}function w5({demoAnnotations:e,demoDelay:t=1e3,enableDemoMode:n=!1,onAnnotationAdd:l,onAnnotationDelete:a,onAnnotationUpdate:o,onAnnotationsClear:i,onCopy:s,onSubmit:u,copyToClipboard:h=!0,endpoint:y,sessionId:S,onSessionCreated:p,webhookUrl:b,className:A}={}){let[k,G]=(0,w.useState)(!1),[f,_]=(0,w.useState)([]),[g,x]=(0,w.useState)(!0),[O,le]=(0,w.useState)(()=>Cg()),[L,U]=(0,w.useState)(!1),W=(0,w.useRef)(null);(0,w.useEffect)(()=>{let c=C=>{let T=W.current;T&&T.contains(C.target)&&C.stopPropagation()},d=["mousedown","click","pointerdown"];return d.forEach(C=>document.body.addEventListener(C,c)),()=>{d.forEach(C=>document.body.removeEventListener(C,c))}},[]);let[$,gt]=(0,w.useState)(!1),[Be,on]=(0,w.useState)(!1),[pt,Xt]=(0,w.useState)(null),[Xl,uu]=(0,w.useState)({x:0,y:0}),[D,be]=(0,w.useState)(null),[fl,Gt]=(0,w.useState)(!1),[sn,cu]=(0,w.useState)("idle"),[tp,Ad]=(0,w.useState)(!1),[zd,Nd]=(0,w.useState)(!1),[ri,ru]=(0,w.useState)(null),[du,ml]=(0,w.useState)(null),[Ld,Ga]=(0,w.useState)([]),[Od,Dd]=(0,w.useState)(null),[di,Bd]=(0,w.useState)(null),[P,Va]=(0,w.useState)(null),[_u,un]=(0,w.useState)(null),[Hd,hl]=(0,w.useState)([]),[yl,Yd]=(0,w.useState)(0),[Rd,Ud]=(0,w.useState)(!1),[He,M5]=(0,w.useState)(!1),[Qt,jd]=(0,w.useState)(!1),[Ka,fu]=(0,w.useState)(!1),[A5,Xd]=(0,w.useState)(!1),[mu,hu]=(0,w.useState)("main"),[Qd,qd]=(0,w.useState)(!1),[z5,yu]=(0,w.useState)(!1),[$d,Zd]=(0,w.useState)(!1),Ql=(0,w.useRef)(null),[Ye,ql]=(0,w.useState)([]),Vt=(0,w.useRef)({cmd:!1,shift:!1}),st=()=>{yu(!0)},N5=()=>{yu(!1)},L5=()=>{$d||(Ql.current=setTimeout(()=>Zd(!0),850))},O5=()=>{Ql.current&&(clearTimeout(Ql.current),Ql.current=null),Zd(!1),N5()};(0,w.useEffect)(()=>()=>{Ql.current&&clearTimeout(Ql.current)},[]);let $l=({content:c,children:d})=>{let[C,T]=(0,w.useState)(!1),[v,z]=(0,w.useState)(!1),[B,Y]=(0,w.useState)(!1),[V,Q]=(0,w.useState)({top:0,right:0}),R=(0,w.useRef)(null),X=(0,w.useRef)(null),K=(0,w.useRef)(null),q=()=>{if(R.current){let Le=R.current.getBoundingClientRect();Q({top:Le.top+Le.height/2,right:window.innerWidth-Le.left+8})}},H=()=>{T(!0),Y(!0),K.current&&(clearTimeout(K.current),K.current=null),q(),X.current=se(()=>{z(!0)},500)},ut=()=>{T(!1),X.current&&(clearTimeout(X.current),X.current=null),z(!1),K.current=se(()=>{Y(!1)},150)};return(0,w.useEffect)(()=>()=>{X.current&&clearTimeout(X.current),K.current&&clearTimeout(K.current)},[]),(0,m.jsxs)(m.Fragment,{children:[(0,m.jsx)("span",{ref:R,onMouseEnter:H,onMouseLeave:ut,children:d}),B&&(0,Sd.createPortal)((0,m.jsx)("div",{"data-feedback-toolbar":!0,style:{position:"fixed",top:V.top,right:V.right,transform:"translateY(-50%)",padding:"6px 10px",background:"#383838",color:"rgba(255, 255, 255, 0.7)",fontSize:"11px",fontWeight:400,lineHeight:"14px",borderRadius:"10px",width:"180px",textAlign:"left",zIndex:100020,pointerEvents:"none",boxShadow:"0px 1px 8px rgba(0, 0, 0, 0.28)",opacity:v&&!Qd?1:0,transition:"opacity 0.15s ease"},children:c}),document.body)]})},[N,Bn]=(0,w.useState)(y5),[I,Gd]=(0,w.useState)(!0),[Vd,Kd]=(0,w.useState)(!1),Zl=!1,cn=Zl&&N.reactEnabled?Fg[N.outputDetail]:"off",[bt,gu]=(0,w.useState)(S??null),Jd=(0,w.useRef)(!1),[lt,gl]=(0,w.useState)(y?"connecting":"disconnected"),[Me,pu]=(0,w.useState)(null),[rn,Wd]=(0,w.useState)(!1),[Gl,Id]=(0,w.useState)(null),[D5,B5]=(0,w.useState)(0),bu=(0,w.useRef)(!1),[Fd,Ja]=(0,w.useState)(new Set),[Pd,_i]=(0,w.useState)(new Set),[Wa,fi]=(0,w.useState)(!1),[H5,Vl]=(0,w.useState)(!1),[dn,e_]=(0,w.useState)(!1),Kl=(0,w.useRef)(null),Kt=(0,w.useRef)(null),Ia=(0,w.useRef)(null),Fa=(0,w.useRef)(null),mi=(0,w.useRef)(!1),t_=(0,w.useRef)(0),hi=(0,w.useRef)(null),n_=(0,w.useRef)(null),vu=8,Y5=50,l_=(0,w.useRef)(null),a_=(0,w.useRef)(null),Pa=(0,w.useRef)(null),ye=typeof window<"u"?window.location.pathname:"/";(0,w.useEffect)(()=>{if(Ka)Xd(!0);else{yu(!1),hu("main");let c=se(()=>Xd(!1),0);return()=>clearTimeout(c)}},[Ka]),(0,w.useEffect)(()=>{qd(!0);let c=se(()=>qd(!1),350);return()=>clearTimeout(c)},[mu]);let o_=k&&g;(0,w.useEffect)(()=>{if(o_){on(!1),gt(!0),Ja(new Set);let c=se(()=>{Ja(d=>{let C=new Set(d);return f.forEach(T=>C.add(T.id)),C})},350);return()=>clearTimeout(c)}else if($){on(!0);let c=se(()=>{gt(!1),on(!1)},250);return()=>clearTimeout(c)}},[o_]),(0,w.useEffect)(()=>{M5(!0),Yd(window.scrollY);let c=hd(ye);_(c.filter(_l)),h5||(Kd(!0),h5=!0,se(()=>Kd(!1),750));try{let d=localStorage.getItem("feedback-toolbar-settings");d&&Bn({...y5,...JSON.parse(d)})}catch{}try{let d=localStorage.getItem("feedback-toolbar-theme");d!==null&&Gd(d==="dark")}catch{}try{let d=localStorage.getItem("feedback-toolbar-position");if(d){let C=JSON.parse(d);typeof C.x=="number"&&typeof C.y=="number"&&pu(C)}}catch{}},[ye]),(0,w.useEffect)(()=>{He&&localStorage.setItem("feedback-toolbar-settings",JSON.stringify(N))},[N,He]),(0,w.useEffect)(()=>{He&&localStorage.setItem("feedback-toolbar-theme",I?"dark":"light")},[I,He]);let i_=(0,w.useRef)(!1);(0,w.useEffect)(()=>{let c=i_.current;i_.current=rn,c&&!rn&&Me&&He&&localStorage.setItem("feedback-toolbar-position",JSON.stringify(Me))},[rn,Me,He]),(0,w.useEffect)(()=>{if(!y||!He||Jd.current)return;Jd.current=!0,gl("connecting"),(async()=>{try{let d=Sg(ye),C=S||d,T=!1;if(C)try{let v=await d5(y,C);gu(v.id),gl("connected"),yd(ye,v.id),T=!0;let z=hd(ye),B=new Set(v.annotations.map(V=>V.id)),Y=z.filter(V=>!B.has(V.id));if(Y.length>0){let Q=`${typeof window<"u"?window.location.origin:""}${ye}`,X=(await Promise.allSettled(Y.map(q=>lu(y,v.id,{...q,sessionId:v.id,url:Q})))).map((q,H)=>q.status==="fulfilled"?q.value:(console.warn("[Agentation] Failed to sync annotation:",q.reason),Y[H])),K=[...v.annotations,...X];_(K.filter(_l)),ai(ye,K.filter(_l),v.id)}else _(v.annotations.filter(_l)),ai(ye,v.annotations.filter(_l),v.id)}catch(v){console.warn("[Agentation] Could not join session, creating new:",v),xg(ye)}if(!T){let v=typeof window<"u"?window.location.href:"/",z=await gd(y,v);gu(z.id),gl("connected"),yd(ye,z.id),p?.(z.id);let B=vg(),Y=typeof window<"u"?window.location.origin:"",V=[];for(let[Q,R]of B){let X=R.filter(H=>!H._syncedTo);if(X.length===0)continue;let K=`${Y}${Q}`,q=Q===ye;V.push((async()=>{try{let H=q?z:await gd(y,K),Hn=(await Promise.allSettled(X.map(et=>lu(y,H.id,{...et,sessionId:H.id,url:K})))).map((et,tt)=>et.status==="fulfilled"?et.value:(console.warn("[Agentation] Failed to sync annotation:",et.reason),X[tt])).filter(_l);if(ai(Q,Hn,H.id),q){let et=new Set(X.map(tt=>tt.id));_(tt=>{let oe=tt.filter(F=>!et.has(F.id));return[...Hn,...oe]})}}catch(H){console.warn(`[Agentation] Failed to sync annotations for ${Q}:`,H)}})())}await Promise.allSettled(V)}}catch(d){gl("disconnected"),console.warn("[Agentation] Failed to initialize session, using local storage:",d)}})()},[y,S,He,p,ye]),(0,w.useEffect)(()=>{if(!y||!He)return;let c=async()=>{try{(await fetch(`${y}/health`)).ok?gl("connected"):gl("disconnected")}catch{gl("disconnected")}};c();let d=rg(c,1e4);return()=>clearInterval(d)},[y,He]),(0,w.useEffect)(()=>{if(!y||!He||!bt)return;let c=new EventSource(`${y}/sessions/${bt}/events`),d=["resolved","dismissed"],C=T=>{try{let v=JSON.parse(T.data);if(d.includes(v.payload?.status)){let z=v.payload.id;_i(B=>new Set(B).add(z)),se(()=>{_(B=>B.filter(Y=>Y.id!==z)),_i(B=>{let Y=new Set(B);return Y.delete(z),Y})},150)}}catch{}};return c.addEventListener("annotation.updated",C),()=>{c.removeEventListener("annotation.updated",C),c.close()}},[y,He,bt]),(0,w.useEffect)(()=>{if(!y||!He)return;let c=n_.current==="disconnected",d=lt==="connected";n_.current=lt,c&&d&&(async()=>{try{let T=hd(ye);if(T.length===0)return;let z=`${typeof window<"u"?window.location.origin:""}${ye}`,B=bt,Y=[];if(B)try{Y=(await d5(y,B)).annotations}catch{B=null}B||(B=(await gd(y,z)).id,gu(B),yd(ye,B));let V=new Set(Y.map(R=>R.id)),Q=T.filter(R=>!V.has(R.id));if(Q.length>0){let X=(await Promise.allSettled(Q.map(H=>lu(y,B,{...H,sessionId:B,url:z})))).map((H,ut)=>H.status==="fulfilled"?H.value:(console.warn("[Agentation] Failed to sync annotation on reconnect:",H.reason),Q[ut])),q=[...Y,...X].filter(_l);_(q),ai(ye,q,B)}}catch(T){console.warn("[Agentation] Failed to sync on reconnect:",T)}})()},[lt,y,He,bt,ye]);let R5=(0,w.useCallback)(()=>{L||(U(!0),fu(!1),G(!1),se(()=>{wg(!0),le(!0),U(!1)},400))},[L]);(0,w.useEffect)(()=>{if(!n||!He||!e||e.length===0||f.length>0)return;let c=[];return c.push(se(()=>{G(!0)},t-200)),e.forEach((d,C)=>{let T=t+C*300;c.push(se(()=>{let v=document.querySelector(d.selector);if(!v)return;let z=v.getBoundingClientRect(),{name:B,path:Y}=iu(v),V={id:`demo-${Date.now()}-${C}`,x:(z.left+z.width/2)/window.innerWidth*100,y:z.top+z.height/2+window.scrollY,comment:d.comment,element:B,elementPath:Y,timestamp:Date.now(),selectedText:d.selectedText,boundingBox:{x:z.left,y:z.top+window.scrollY,width:z.width,height:z.height},nearbyText:ni(v),cssClasses:li(v)};_(Q=>[...Q,V])},T))}),()=>{c.forEach(clearTimeout)}},[n,He,e,t]),(0,w.useEffect)(()=>{let c=()=>{Yd(window.scrollY),Ud(!0),Pa.current&&clearTimeout(Pa.current),Pa.current=se(()=>{Ud(!1)},150)};return window.addEventListener("scroll",c,{passive:!0}),()=>{window.removeEventListener("scroll",c),Pa.current&&clearTimeout(Pa.current)}},[]),(0,w.useEffect)(()=>{He&&f.length>0?bt?ai(ye,f,bt):S5(ye,f):He&&f.length===0&&localStorage.removeItem(su(ye))},[f,ye,He,bt]);let s_=(0,w.useCallback)(()=>{Qt||(_g(),jd(!0))},[Qt]),yi=(0,w.useCallback)(()=>{Qt&&(c5(),jd(!1))},[Qt]),Su=(0,w.useCallback)(()=>{Qt?yi():s_()},[Qt,s_,yi]),u_=(0,w.useCallback)(()=>{if(Ye.length===0)return;let c=Ye[0],d=c.element,C=Ye.length>1,T=Ye.map(v=>v.element.getBoundingClientRect());if(C){let v={left:Math.min(...T.map(H=>H.left)),top:Math.min(...T.map(H=>H.top)),right:Math.max(...T.map(H=>H.right)),bottom:Math.max(...T.map(H=>H.bottom))},z=Ye.slice(0,5).map(H=>H.name).join(", "),B=Ye.length>5?` +${Ye.length-5} more`:"",Y=T.map(H=>({x:H.left,y:H.top+window.scrollY,width:H.width,height:H.height})),Q=Ye[Ye.length-1].element,R=T[T.length-1],X=R.left+R.width/2,K=R.top+R.height/2,q=vd(Q);be({x:X/window.innerWidth*100,y:q?K:K+window.scrollY,clientY:K,element:`${Ye.length} elements: ${z}${B}`,elementPath:"multi-select",boundingBox:{x:v.left,y:v.top+window.scrollY,width:v.right-v.left,height:v.bottom-v.top},isMultiSelect:!0,isFixed:q,elementBoundingBoxes:Y,multiSelectElements:Ye.map(H=>H.element),targetElement:Q,fullPath:nu(d),accessibility:tu(d),computedStyles:eu(d),computedStylesObj:Ps(d),nearbyElements:Fs(d),cssClasses:li(d),nearbyText:ni(d),sourceFile:ou(d)})}else{let v=T[0],z=vd(d);be({x:v.left/window.innerWidth*100,y:z?v.top:v.top+window.scrollY,clientY:v.top,element:c.name,elementPath:c.path,boundingBox:{x:v.left,y:z?v.top:v.top+window.scrollY,width:v.width,height:v.height},isFixed:z,fullPath:nu(d),accessibility:tu(d),computedStyles:eu(d),computedStylesObj:Ps(d),nearbyElements:Fs(d),cssClasses:li(d),nearbyText:ni(d),reactComponents:c.reactComponents,sourceFile:ou(d)})}ql([]),Xt(null)},[Ye]);(0,w.useEffect)(()=>{k||(be(null),Va(null),un(null),hl([]),Xt(null),fu(!1),ql([]),Vt.current={cmd:!1,shift:!1},Qt&&yi())},[k,Qt,yi]),(0,w.useEffect)(()=>()=>{c5()},[]),(0,w.useEffect)(()=>{if(!k)return;let c=document.createElement("style");return c.id="feedback-cursor-styles",c.textContent=`
      body * {
        cursor: crosshair !important;
      }
      body p, body span, body h1, body h2, body h3, body h4, body h5, body h6,
      body li, body td, body th, body label, body blockquote, body figcaption,
      body caption, body legend, body dt, body dd, body pre, body code,
      body em, body strong, body b, body i, body u, body s, body a,
      body time, body address, body cite, body q, body abbr, body dfn,
      body mark, body small, body sub, body sup, body [contenteditable],
      body p *, body span *, body h1 *, body h2 *, body h3 *, body h4 *,
      body h5 *, body h6 *, body li *, body a *, body label *, body pre *,
      body code *, body blockquote *, body [contenteditable] * {
        cursor: text !important;
      }
      [data-feedback-toolbar], [data-feedback-toolbar] * {
        cursor: default !important;
      }
      [data-feedback-toolbar] textarea,
      [data-feedback-toolbar] input[type="text"],
      [data-feedback-toolbar] input[type="url"] {
        cursor: text !important;
      }
      [data-feedback-toolbar] button,
      [data-feedback-toolbar] button *,
      [data-feedback-toolbar] label,
      [data-feedback-toolbar] label *,
      [data-feedback-toolbar] a,
      [data-feedback-toolbar] a *,
      [data-feedback-toolbar] [role="button"],
      [data-feedback-toolbar] [role="button"] * {
        cursor: pointer !important;
      }
      [data-annotation-marker], [data-annotation-marker] * {
        cursor: pointer !important;
      }
    `,document.head.appendChild(c),()=>{let d=document.getElementById("feedback-cursor-styles");d&&d.remove()}},[k]),(0,w.useEffect)(()=>{if(!k||D)return;let c=d=>{let C=d.composedPath()[0]||d.target;if(yt(C,"[data-feedback-toolbar]")){Xt(null);return}let T=$a(d.clientX,d.clientY);if(!T||yt(T,"[data-feedback-toolbar]")){Xt(null);return}let{name:v,elementName:z,path:B,reactComponents:Y}=bd(T,cn),V=T.getBoundingClientRect();Xt({element:v,elementName:z,elementPath:B,rect:V,reactComponents:Y}),uu({x:d.clientX,y:d.clientY})};return document.addEventListener("mousemove",c),()=>document.removeEventListener("mousemove",c)},[k,D,cn]),(0,w.useEffect)(()=>{if(!k)return;let c=d=>{if(mi.current){mi.current=!1;return}let C=d.composedPath()[0]||d.target;if(yt(C,"[data-feedback-toolbar]")||yt(C,"[data-annotation-popup]")||yt(C,"[data-annotation-marker]"))return;if(d.metaKey&&d.shiftKey&&!D&&!P){d.preventDefault(),d.stopPropagation();let Le=$a(d.clientX,d.clientY);if(!Le)return;let Hn=Le.getBoundingClientRect(),{name:et,path:tt,reactComponents:oe}=bd(Le,cn),F=Ye.findIndex(Ze=>Ze.element===Le);F>=0?ql(Ze=>Ze.filter((Re,Yn)=>Yn!==F)):ql(Ze=>[...Ze,{element:Le,rect:Hn,name:et,path:tt,reactComponents:oe??void 0}]);return}let T=yt(C,"button, a, input, select, textarea, [role='button'], [onclick]");if(N.blockInteractions&&T&&(d.preventDefault(),d.stopPropagation()),D){if(T&&!N.blockInteractions)return;d.preventDefault(),l_.current?.shake();return}if(P){if(T&&!N.blockInteractions)return;d.preventDefault(),a_.current?.shake();return}d.preventDefault();let v=$a(d.clientX,d.clientY);if(!v)return;let{name:z,path:B,reactComponents:Y}=bd(v,cn),V=v.getBoundingClientRect(),Q=d.clientX/window.innerWidth*100,R=vd(v),X=R?d.clientY:d.clientY+window.scrollY,K=window.getSelection(),q;K&&K.toString().trim().length>0&&(q=K.toString().trim().slice(0,500));let H=Ps(v),ut=eu(v);be({x:Q,y:X,clientY:d.clientY,element:z,elementPath:B,selectedText:q,boundingBox:{x:V.left,y:R?V.top:V.top+window.scrollY,width:V.width,height:V.height},nearbyText:ni(v),cssClasses:li(v),isFixed:R,fullPath:nu(v),accessibility:tu(v),computedStyles:ut,computedStylesObj:H,nearbyElements:Fs(v),reactComponents:Y??void 0,sourceFile:ou(v),targetElement:v}),Xt(null)};return document.addEventListener("click",c,!0),()=>document.removeEventListener("click",c,!0)},[k,D,P,N.blockInteractions,cn,Ye]),(0,w.useEffect)(()=>{if(!k)return;let c=T=>{T.key==="Meta"&&(Vt.current.cmd=!0),T.key==="Shift"&&(Vt.current.shift=!0)},d=T=>{let v=Vt.current.cmd&&Vt.current.shift;T.key==="Meta"&&(Vt.current.cmd=!1),T.key==="Shift"&&(Vt.current.shift=!1);let z=Vt.current.cmd&&Vt.current.shift;v&&!z&&Ye.length>0&&u_()},C=()=>{Vt.current={cmd:!1,shift:!1},ql([])};return document.addEventListener("keydown",c),document.addEventListener("keyup",d),window.addEventListener("blur",C),()=>{document.removeEventListener("keydown",c),document.removeEventListener("keyup",d),window.removeEventListener("blur",C)}},[k,Ye,u_]),(0,w.useEffect)(()=>{if(!k||D)return;let c=d=>{let C=d.composedPath()[0]||d.target;yt(C,"[data-feedback-toolbar]")||yt(C,"[data-annotation-marker]")||yt(C,"[data-annotation-popup]")||new Set(["P","SPAN","H1","H2","H3","H4","H5","H6","LI","TD","TH","LABEL","BLOCKQUOTE","FIGCAPTION","CAPTION","LEGEND","DT","DD","PRE","CODE","EM","STRONG","B","I","U","S","A","TIME","ADDRESS","CITE","Q","ABBR","DFN","MARK","SMALL","SUB","SUP"]).has(C.tagName)||C.isContentEditable||(Kl.current={x:d.clientX,y:d.clientY})};return document.addEventListener("mousedown",c),()=>document.removeEventListener("mousedown",c)},[k,D]),(0,w.useEffect)(()=>{if(!k||D)return;let c=d=>{if(!Kl.current)return;let C=d.clientX-Kl.current.x,T=d.clientY-Kl.current.y,v=C*C+T*T,z=vu*vu;if(!dn&&v>=z&&(Kt.current=Kl.current,e_(!0)),(dn||v>=z)&&Kt.current){if(Ia.current){let oe=Math.min(Kt.current.x,d.clientX),F=Math.min(Kt.current.y,d.clientY),Ze=Math.abs(d.clientX-Kt.current.x),Re=Math.abs(d.clientY-Kt.current.y);Ia.current.style.transform=`translate(${oe}px, ${F}px)`,Ia.current.style.width=`${Ze}px`,Ia.current.style.height=`${Re}px`}let B=Date.now();if(B-t_.current<Y5)return;t_.current=B;let Y=Kt.current.x,V=Kt.current.y,Q=Math.min(Y,d.clientX),R=Math.min(V,d.clientY),X=Math.max(Y,d.clientX),K=Math.max(V,d.clientY),q=(Q+X)/2,H=(R+K)/2,ut=new Set,Le=[[Q,R],[X,R],[Q,K],[X,K],[q,H],[q,R],[q,K],[Q,H],[X,H]];for(let[oe,F]of Le){let Ze=document.elementsFromPoint(oe,F);for(let Re of Ze)Re instanceof HTMLElement&&ut.add(Re)}let Hn=document.querySelectorAll("button, a, input, img, p, h1, h2, h3, h4, h5, h6, li, label, td, th, div, span, section, article, aside, nav");for(let oe of Hn)if(oe instanceof HTMLElement){let F=oe.getBoundingClientRect(),Ze=F.left+F.width/2,Re=F.top+F.height/2,Yn=Ze>=Q&&Ze<=X&&Re>=R&&Re<=K,_n=Math.min(F.right,X)-Math.max(F.left,Q),d_=Math.min(F.bottom,K)-Math.max(F.top,R),$5=_n>0&&d_>0?_n*d_:0,__=F.width*F.height,Z5=__>0?$5/__:0;(Yn||Z5>.5)&&ut.add(oe)}let et=[],tt=new Set(["BUTTON","A","INPUT","IMG","P","H1","H2","H3","H4","H5","H6","LI","LABEL","TD","TH","SECTION","ARTICLE","ASIDE","NAV"]);for(let oe of ut){if(yt(oe,"[data-feedback-toolbar]")||yt(oe,"[data-annotation-marker]"))continue;let F=oe.getBoundingClientRect();if(!(F.width>window.innerWidth*.8&&F.height>window.innerHeight*.5)&&!(F.width<10||F.height<10)&&F.left<X&&F.right>Q&&F.top<K&&F.bottom>R){let Ze=oe.tagName,Re=tt.has(Ze);if(!Re&&(Ze==="DIV"||Ze==="SPAN")){let Yn=oe.textContent&&oe.textContent.trim().length>0,_n=oe.onclick!==null||oe.getAttribute("role")==="button"||oe.getAttribute("role")==="link"||oe.classList.contains("clickable")||oe.hasAttribute("data-clickable");(Yn||_n)&&!oe.querySelector("p, h1, h2, h3, h4, h5, h6, button, a")&&(Re=!0)}if(Re){let Yn=!1;for(let _n of et)if(_n.left<=F.left&&_n.right>=F.right&&_n.top<=F.top&&_n.bottom>=F.bottom){Yn=!0;break}Yn||et.push(F)}}}if(Fa.current){let oe=Fa.current;for(;oe.children.length>et.length;)oe.removeChild(oe.lastChild);et.forEach((F,Ze)=>{let Re=oe.children[Ze];Re||(Re=document.createElement("div"),Re.className=r.selectedElementHighlight,oe.appendChild(Re)),Re.style.transform=`translate(${F.left}px, ${F.top}px)`,Re.style.width=`${F.width}px`,Re.style.height=`${F.height}px`})}}};return document.addEventListener("mousemove",c,{passive:!0}),()=>document.removeEventListener("mousemove",c)},[k,D,dn,vu]),(0,w.useEffect)(()=>{if(!k)return;let c=d=>{let C=dn,T=Kt.current;if(dn&&T){mi.current=!0;let v=Math.min(T.x,d.clientX),z=Math.min(T.y,d.clientY),B=Math.max(T.x,d.clientX),Y=Math.max(T.y,d.clientY),V=[];document.querySelectorAll("button, a, input, img, p, h1, h2, h3, h4, h5, h6, li, label, td, th").forEach(q=>{if(!(q instanceof HTMLElement)||yt(q,"[data-feedback-toolbar]")||yt(q,"[data-annotation-marker]"))return;let H=q.getBoundingClientRect();H.width>window.innerWidth*.8&&H.height>window.innerHeight*.5||H.width<10||H.height<10||H.left<B&&H.right>v&&H.top<Y&&H.bottom>z&&V.push({element:q,rect:H})});let R=V.filter(({element:q})=>!V.some(({element:H})=>H!==q&&q.contains(H))),X=d.clientX/window.innerWidth*100,K=d.clientY+window.scrollY;if(R.length>0){let q=R.reduce((tt,{rect:oe})=>({left:Math.min(tt.left,oe.left),top:Math.min(tt.top,oe.top),right:Math.max(tt.right,oe.right),bottom:Math.max(tt.bottom,oe.bottom)}),{left:1/0,top:1/0,right:-1/0,bottom:-1/0}),H=R.slice(0,5).map(({element:tt})=>iu(tt).name).join(", "),ut=R.length>5?` +${R.length-5} more`:"",Le=R[0].element,Hn=Ps(Le),et=eu(Le);be({x:X,y:K,clientY:d.clientY,element:`${R.length} elements: ${H}${ut}`,elementPath:"multi-select",boundingBox:{x:q.left,y:q.top+window.scrollY,width:q.right-q.left,height:q.bottom-q.top},isMultiSelect:!0,fullPath:nu(Le),accessibility:tu(Le),computedStyles:et,computedStylesObj:Hn,nearbyElements:Fs(Le),cssClasses:li(Le),nearbyText:ni(Le),sourceFile:ou(Le)})}else{let q=Math.abs(B-v),H=Math.abs(Y-z);q>20&&H>20&&be({x:X,y:K,clientY:d.clientY,element:"Area selection",elementPath:`region at (${Math.round(v)}, ${Math.round(z)})`,boundingBox:{x:v,y:z+window.scrollY,width:q,height:H},isMultiSelect:!0})}Xt(null)}else C&&(mi.current=!0);Kl.current=null,Kt.current=null,e_(!1),Fa.current&&(Fa.current.innerHTML="")};return document.addEventListener("mouseup",c),()=>document.removeEventListener("mouseup",c)},[k,dn]);let Jt=(0,w.useCallback)(async(c,d,C)=>{let T=N.webhookUrl||b;if(!T||!N.webhooksEnabled&&!C)return!1;try{return(await fetch(T,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({event:c,timestamp:Date.now(),url:typeof window<"u"?window.location.href:void 0,...d})})).ok}catch(v){return console.warn("[Agentation] Webhook failed:",v),!1}},[b,N.webhookUrl,N.webhooksEnabled]),U5=(0,w.useCallback)(c=>{if(!D)return;let d={id:Date.now().toString(),x:D.x,y:D.y,comment:c,element:D.element,elementPath:D.elementPath,timestamp:Date.now(),selectedText:D.selectedText,boundingBox:D.boundingBox,nearbyText:D.nearbyText,cssClasses:D.cssClasses,isMultiSelect:D.isMultiSelect,isFixed:D.isFixed,fullPath:D.fullPath,accessibility:D.accessibility,computedStyles:D.computedStyles,nearbyElements:D.nearbyElements,reactComponents:D.reactComponents,sourceFile:D.sourceFile,elementBoundingBoxes:D.elementBoundingBoxes,...y&&bt?{sessionId:bt,url:typeof window<"u"?window.location.href:void 0,status:"pending"}:{}};_(C=>[...C,d]),hi.current=d.id,se(()=>{hi.current=null},300),se(()=>{Ja(C=>new Set(C).add(d.id))},250),l?.(d),Jt("annotation.add",{annotation:d}),fi(!0),se(()=>{be(null),fi(!1)},150),window.getSelection()?.removeAllRanges(),y&&bt&&lu(y,bt,d).then(C=>{C.id!==d.id&&(_(T=>T.map(v=>v.id===d.id?{...v,id:C.id}:v)),Ja(T=>{let v=new Set(T);return v.delete(d.id),v.add(C.id),v}))}).catch(C=>{console.warn("[Agentation] Failed to sync annotation:",C)})},[D,l,Jt,y,bt]),j5=(0,w.useCallback)(()=>{fi(!0),se(()=>{be(null),fi(!1)},150)},[]),xu=(0,w.useCallback)(c=>{let d=f.findIndex(T=>T.id===c),C=f[d];P?.id===c&&(Vl(!0),se(()=>{Va(null),un(null),hl([]),Vl(!1)},150)),Dd(c),_i(T=>new Set(T).add(c)),C&&(a?.(C),Jt("annotation.delete",{annotation:C})),y&&_5(y,c).catch(T=>{console.warn("[Agentation] Failed to delete annotation from server:",T)}),se(()=>{_(T=>T.filter(v=>v.id!==c)),_i(T=>{let v=new Set(T);return v.delete(c),v}),Dd(null),d<f.length-1&&(Bd(d),se(()=>Bd(null),200))},150)},[f,P,a,Jt,y]),gi=(0,w.useCallback)(c=>{if(Va(c),ru(null),ml(null),Ga([]),c.elementBoundingBoxes?.length){let d=[];for(let C of c.elementBoundingBoxes){let T=C.x+C.width/2,v=C.y+C.height/2-window.scrollY,z=$a(T,v);z&&d.push(z)}hl(d),un(null)}else if(c.boundingBox){let d=c.boundingBox,C=d.x+d.width/2,T=c.isFixed?d.y+d.height/2:d.y+d.height/2-window.scrollY,v=$a(C,T);if(v){let z=v.getBoundingClientRect(),B=z.width/d.width,Y=z.height/d.height;B<.5||Y<.5?un(null):un(v)}else un(null);hl([])}else un(null),hl([])},[]),pi=(0,w.useCallback)(c=>{if(!c){ru(null),ml(null),Ga([]);return}if(ru(c.id),c.elementBoundingBoxes?.length){let d=[];for(let C of c.elementBoundingBoxes){let T=C.x+C.width/2,v=C.y+C.height/2-window.scrollY,B=document.elementsFromPoint(T,v).find(Y=>!Y.closest("[data-annotation-marker]")&&!Y.closest("[data-agentation-root]"));B&&d.push(B)}Ga(d),ml(null)}else if(c.boundingBox){let d=c.boundingBox,C=d.x+d.width/2,T=c.isFixed?d.y+d.height/2:d.y+d.height/2-window.scrollY,v=$a(C,T);if(v){let z=v.getBoundingClientRect(),B=z.width/d.width,Y=z.height/d.height;B<.5||Y<.5?ml(null):ml(v)}else ml(null);Ga([])}else ml(null),Ga([])},[]),X5=(0,w.useCallback)(c=>{if(!P)return;let d={...P,comment:c};_(C=>C.map(T=>T.id===P.id?d:T)),o?.(d),Jt("annotation.update",{annotation:d}),y&&Eg(y,P.id,{comment:c}).catch(C=>{console.warn("[Agentation] Failed to update annotation on server:",C)}),Vl(!0),se(()=>{Va(null),un(null),hl([]),Vl(!1)},150)},[P,o,Jt,y]),Q5=(0,w.useCallback)(()=>{Vl(!0),se(()=>{Va(null),un(null),hl([]),Vl(!1)},150)},[]),pl=(0,w.useCallback)(()=>{let c=f.length;if(c===0)return;i?.(f),Jt("annotations.clear",{annotations:f}),y&&Promise.all(f.map(C=>_5(y,C.id).catch(T=>{console.warn("[Agentation] Failed to delete annotation from server:",T)}))),Nd(!0),Ad(!0);let d=c*30+200;se(()=>{_([]),Ja(new Set),localStorage.removeItem(su(ye)),Nd(!1)},d),se(()=>Ad(!1),1500)},[ye,f,i,Jt,y]),Cu=(0,w.useCallback)(async()=>{let c=typeof window<"u"?window.location.pathname+window.location.search+window.location.hash:ye,d=g5(f,c,N.outputDetail,cn);if(d){if(h)try{await navigator.clipboard.writeText(d)}catch{}s?.(d),Gt(!0),se(()=>Gt(!1),2e3),N.autoClearAfterCopy&&se(()=>pl(),500)}},[f,ye,N.outputDetail,cn,N.autoClearAfterCopy,pl,h,s]),wu=(0,w.useCallback)(async()=>{let c=typeof window<"u"?window.location.pathname+window.location.search+window.location.hash:ye,d=g5(f,c,N.outputDetail,cn);if(!d)return;u&&u(d,f),cu("sending"),await new Promise(T=>se(T,150));let C=await Jt("submit",{output:d,annotations:f},!0);cu(C?"sent":"failed"),se(()=>cu("idle"),2500),C&&N.autoClearAfterCopy&&se(()=>pl(),500)},[u,Jt,f,ye,N.outputDetail,cn,N.autoClearAfterCopy,pl]);(0,w.useEffect)(()=>{if(!Gl)return;let c=10,d=T=>{let v=T.clientX-Gl.x,z=T.clientY-Gl.y,B=Math.sqrt(v*v+z*z);if(!rn&&B>c&&Wd(!0),rn||B>c){let Y=Gl.toolbarX+v,V=Gl.toolbarY+z,Q=20,R=297,X=44,q=R-(k?lt==="connected"?297:257:44),H=Q-q,ut=window.innerWidth-Q-R;Y=Math.max(H,Math.min(ut,Y)),V=Math.max(Q,Math.min(window.innerHeight-X-Q,V)),pu({x:Y,y:V})}},C=()=>{rn&&(bu.current=!0),Wd(!1),Id(null)};return document.addEventListener("mousemove",d),document.addEventListener("mouseup",C),()=>{document.removeEventListener("mousemove",d),document.removeEventListener("mouseup",C)}},[Gl,rn,k,lt]);let q5=(0,w.useCallback)(c=>{if(c.target.closest("button")||c.target.closest(`.${r.settingsPanel}`))return;let d=c.currentTarget.parentElement;if(!d)return;let C=d.getBoundingClientRect(),T=Me?.x??C.left,v=Me?.y??C.top,z=(Math.random()-.5)*10;B5(z),Id({x:c.clientX,y:c.clientY,toolbarX:T,toolbarY:v})},[Me]);if((0,w.useEffect)(()=>{if(!Me)return;let c=()=>{let v=Me.x,z=Me.y,V=20-(297-(k?lt==="connected"?297:257:44)),Q=window.innerWidth-20-297;v=Math.max(V,Math.min(Q,v)),z=Math.max(20,Math.min(window.innerHeight-44-20,z)),(v!==Me.x||z!==Me.y)&&pu({x:v,y:z})};return c(),window.addEventListener("resize",c),()=>window.removeEventListener("resize",c)},[Me,k,lt]),(0,w.useEffect)(()=>{let c=d=>{let C=d.target,T=C.tagName==="INPUT"||C.tagName==="TEXTAREA"||C.isContentEditable;if(d.key==="Escape"){if(Ye.length>0){ql([]);return}D||k&&(st(),G(!1))}if((d.metaKey||d.ctrlKey)&&d.shiftKey&&(d.key==="f"||d.key==="F")){d.preventDefault(),st(),G(v=>!v);return}if(!(T||d.metaKey||d.ctrlKey)&&((d.key==="p"||d.key==="P")&&(d.preventDefault(),st(),Su()),(d.key==="h"||d.key==="H")&&f.length>0&&(d.preventDefault(),st(),x(v=>!v)),(d.key==="c"||d.key==="C")&&f.length>0&&(d.preventDefault(),st(),Cu()),(d.key==="x"||d.key==="X")&&f.length>0&&(d.preventDefault(),st(),pl()),d.key==="s"||d.key==="S")){let v=an(N.webhookUrl)||an(b||"");f.length>0&&v&&sn==="idle"&&(d.preventDefault(),st(),wu())}};return document.addEventListener("keydown",c),()=>document.removeEventListener("keydown",c)},[k,D,f.length,N.webhookUrl,b,sn,wu,Su,Cu,pl,Ye]),!He||O)return null;let Jl=f.length>0,bi=f.filter(c=>!Pd.has(c.id)&&_l(c)),c_=f.filter(c=>Pd.has(c.id)),r_=c=>{let z=c.x/100*window.innerWidth,B=typeof c.y=="string"?parseFloat(c.y):c.y,Y={};window.innerHeight-B-22-10<80&&(Y.top="auto",Y.bottom="calc(100% + 10px)");let Q=z-200/2,R=10;if(Q<R){let X=R-Q;Y.left=`calc(50% + ${X}px)`}else if(Q+200>window.innerWidth-R){let X=Q+200-(window.innerWidth-R);Y.left=`calc(50% - ${X}px)`}return Y};return(0,Sd.createPortal)((0,m.jsxs)("div",{ref:W,style:{display:"contents"},children:[(0,m.jsx)("div",{className:`${r.toolbar}${A?` ${A}`:""}`,"data-feedback-toolbar":!0,style:Me?{left:Me.x,top:Me.y,right:"auto",bottom:"auto"}:void 0,children:(0,m.jsxs)("div",{className:`${r.toolbarContainer} ${I?"":r.light} ${k?r.expanded:r.collapsed} ${Vd?r.entrance:""} ${L?r.hiding:""} ${rn?r.dragging:""} ${!N.webhooksEnabled&&(an(N.webhookUrl)||an(b||""))?r.serverConnected:""}`,onClick:k?void 0:c=>{if(bu.current){bu.current=!1,c.preventDefault();return}G(!0)},onMouseDown:q5,role:k?void 0:"button",tabIndex:k?-1:0,title:k?void 0:"Start feedback mode",style:{...rn&&{transform:`scale(1.05) rotate(${D5}deg)`,cursor:"grabbing"}},children:[(0,m.jsxs)("div",{className:`${r.toggleContent} ${k?r.hidden:r.visible}`,children:[(0,m.jsx)(Iy,{size:24}),Jl&&(0,m.jsx)("span",{className:`${r.badge} ${k?r.fadeOut:""} ${Vd?r.entrance:""}`,style:{backgroundColor:N.annotationColor},children:f.length})]}),(0,m.jsxs)("div",{className:`${r.controlsContent} ${k?r.visible:r.hidden} ${Me&&Me.y<100?r.tooltipBelow:""} ${z5||Ka?r.tooltipsHidden:""} ${$d?r.tooltipsInSession:""}`,onMouseEnter:L5,onMouseLeave:O5,children:[(0,m.jsxs)("div",{className:`${r.buttonWrapper} ${Me&&Me.x<120?r.buttonWrapperAlignLeft:""}`,children:[(0,m.jsx)("button",{className:`${r.controlButton} ${I?"":r.light}`,onClick:c=>{c.stopPropagation(),st(),Su()},"data-active":Qt,children:(0,m.jsx)(tg,{size:24,isPaused:Qt})}),(0,m.jsxs)("span",{className:r.buttonTooltip,children:[Qt?"Resume animations":"Pause animations",(0,m.jsx)("span",{className:r.shortcut,children:"P"})]})]}),(0,m.jsxs)("div",{className:r.buttonWrapper,children:[(0,m.jsx)("button",{className:`${r.controlButton} ${I?"":r.light}`,onClick:c=>{c.stopPropagation(),st(),x(!g)},disabled:!Jl,children:(0,m.jsx)(eg,{size:24,isOpen:g})}),(0,m.jsxs)("span",{className:r.buttonTooltip,children:[g?"Hide markers":"Show markers",(0,m.jsx)("span",{className:r.shortcut,children:"H"})]})]}),(0,m.jsxs)("div",{className:r.buttonWrapper,children:[(0,m.jsx)("button",{className:`${r.controlButton} ${I?"":r.light} ${fl?r.statusShowing:""}`,onClick:c=>{c.stopPropagation(),st(),Cu()},disabled:!Jl,"data-active":fl,children:(0,m.jsx)(Fy,{size:24,copied:fl})}),(0,m.jsxs)("span",{className:r.buttonTooltip,children:["Copy feedback",(0,m.jsx)("span",{className:r.shortcut,children:"C"})]})]}),(0,m.jsxs)("div",{className:`${r.buttonWrapper} ${r.sendButtonWrapper} ${k&&!N.webhooksEnabled&&(an(N.webhookUrl)||an(b||""))?r.sendButtonVisible:""}`,children:[(0,m.jsxs)("button",{className:`${r.controlButton} ${I?"":r.light} ${sn==="sent"||sn==="failed"?r.statusShowing:""}`,onClick:c=>{c.stopPropagation(),st(),wu()},disabled:!Jl||!an(N.webhookUrl)&&!an(b||"")||sn==="sending","data-no-hover":sn==="sent"||sn==="failed",tabIndex:an(N.webhookUrl)||an(b||"")?0:-1,children:[(0,m.jsx)(Py,{size:24,state:sn}),Jl&&sn==="idle"&&(0,m.jsx)("span",{className:`${r.buttonBadge} ${I?"":r.light}`,style:{backgroundColor:N.annotationColor},children:f.length})]}),(0,m.jsxs)("span",{className:r.buttonTooltip,children:["Send Annotations",(0,m.jsx)("span",{className:r.shortcut,children:"S"})]})]}),(0,m.jsxs)("div",{className:r.buttonWrapper,children:[(0,m.jsx)("button",{className:`${r.controlButton} ${I?"":r.light}`,onClick:c=>{c.stopPropagation(),st(),pl()},disabled:!Jl,"data-danger":!0,children:(0,m.jsx)(lg,{size:24})}),(0,m.jsxs)("span",{className:r.buttonTooltip,children:["Clear all",(0,m.jsx)("span",{className:r.shortcut,children:"X"})]})]}),(0,m.jsxs)("div",{className:r.buttonWrapper,children:[(0,m.jsx)("button",{className:`${r.controlButton} ${I?"":r.light}`,onClick:c=>{c.stopPropagation(),st(),fu(!Ka)},children:(0,m.jsx)(ng,{size:24})}),y&&lt!=="disconnected"&&(0,m.jsx)("span",{className:`${r.mcpIndicator} ${I?"":r.light} ${r[lt]} ${Ka?r.hidden:""}`,title:lt==="connected"?"MCP Connected":"MCP Connecting..."}),(0,m.jsx)("span",{className:r.buttonTooltip,children:"Settings"})]}),(0,m.jsx)("div",{className:`${r.divider} ${I?"":r.light}`}),(0,m.jsxs)("div",{className:`${r.buttonWrapper} ${Me&&typeof window<"u"&&Me.x>window.innerWidth-120?r.buttonWrapperAlignRight:""}`,children:[(0,m.jsx)("button",{className:`${r.controlButton} ${I?"":r.light}`,onClick:c=>{c.stopPropagation(),st(),G(!1)},children:(0,m.jsx)(ag,{size:24})}),(0,m.jsxs)("span",{className:r.buttonTooltip,children:["Exit",(0,m.jsx)("span",{className:r.shortcut,children:"Esc"})]})]})]}),(0,m.jsx)("div",{className:`${r.settingsPanel} ${I?r.dark:r.light} ${A5?r.enter:r.exit}`,onClick:c=>c.stopPropagation(),style:Me&&Me.y<230?{bottom:"auto",top:"calc(100% + 0.5rem)"}:void 0,children:(0,m.jsxs)("div",{className:`${r.settingsPanelContainer} ${Qd?r.transitioning:""}`,children:[(0,m.jsxs)("div",{className:`${r.settingsPage} ${mu==="automations"?r.slideLeft:""}`,children:[(0,m.jsxs)("div",{className:r.settingsHeader,children:[(0,m.jsxs)("span",{className:r.settingsBrand,children:[(0,m.jsx)("span",{className:r.settingsBrandSlash,style:{color:N.annotationColor,transition:"color 0.2s ease"},children:"/"}),"agentation"]}),(0,m.jsxs)("span",{className:r.settingsVersion,children:["v","2.3.2"]}),(0,m.jsx)("button",{className:r.themeToggle,onClick:()=>Gd(!I),title:I?"Switch to light mode":"Switch to dark mode",children:(0,m.jsx)("span",{className:r.themeIconWrapper,children:(0,m.jsx)("span",{className:r.themeIcon,children:I?(0,m.jsx)(og,{size:20}):(0,m.jsx)(ig,{size:20})},I?"sun":"moon")})})]}),(0,m.jsxs)("div",{className:r.settingsSection,children:[(0,m.jsxs)("div",{className:r.settingsRow,children:[(0,m.jsxs)("div",{className:`${r.settingsLabel} ${I?"":r.light}`,children:["Output Detail",(0,m.jsx)($l,{content:"Controls how much detail is included in the copied output",children:(0,m.jsx)("span",{className:r.helpIcon,children:(0,m.jsx)(Qa,{size:20})})})]}),(0,m.jsxs)("button",{className:`${r.cycleButton} ${I?"":r.light}`,onClick:()=>{let d=(si.findIndex(C=>C.value===N.outputDetail)+1)%si.length;Bn(C=>({...C,outputDetail:si[d].value}))},children:[(0,m.jsx)("span",{className:r.cycleButtonText,children:si.find(c=>c.value===N.outputDetail)?.label},N.outputDetail),(0,m.jsx)("span",{className:r.cycleDots,children:si.map((c,d)=>(0,m.jsx)("span",{className:`${r.cycleDot} ${I?"":r.light} ${N.outputDetail===c.value?r.active:""}`},c.value))})]})]}),(0,m.jsxs)("div",{className:`${r.settingsRow} ${r.settingsRowMarginTop} ${Zl?"":r.settingsRowDisabled}`,children:[(0,m.jsxs)("div",{className:`${r.settingsLabel} ${I?"":r.light}`,children:["React Components",(0,m.jsx)($l,{content:Zl?"Include React component names in annotations":"Disabled \u2014 production builds minify component names, making detection unreliable. Use in development mode.",children:(0,m.jsx)("span",{className:r.helpIcon,children:(0,m.jsx)(Qa,{size:20})})})]}),(0,m.jsxs)("label",{className:`${r.toggleSwitch} ${Zl?"":r.disabled}`,children:[(0,m.jsx)("input",{type:"checkbox",checked:Zl&&N.reactEnabled,disabled:!Zl,onChange:()=>Bn(c=>({...c,reactEnabled:!c.reactEnabled}))}),(0,m.jsx)("span",{className:r.toggleSlider})]})]}),(0,m.jsxs)("div",{className:`${r.settingsRow} ${r.settingsRowMarginTop}`,children:[(0,m.jsxs)("div",{className:`${r.settingsLabel} ${I?"":r.light}`,children:["Hide Until Restart",(0,m.jsx)($l,{content:"Hides the toolbar until you open a new tab",children:(0,m.jsx)("span",{className:r.helpIcon,children:(0,m.jsx)(Qa,{size:20})})})]}),(0,m.jsxs)("label",{className:r.toggleSwitch,children:[(0,m.jsx)("input",{type:"checkbox",checked:!1,onChange:c=>{c.target.checked&&R5()}}),(0,m.jsx)("span",{className:r.toggleSlider})]})]})]}),(0,m.jsxs)("div",{className:r.settingsSection,children:[(0,m.jsx)("div",{className:`${r.settingsLabel} ${r.settingsLabelMarker} ${I?"":r.light}`,children:"Marker Colour"}),(0,m.jsx)("div",{className:r.colorOptions,children:Pg.map(c=>(0,m.jsx)("div",{role:"button",onClick:()=>Bn(d=>({...d,annotationColor:c.value})),style:{borderColor:N.annotationColor===c.value?c.value:"transparent"},className:`${r.colorOptionRing} ${N.annotationColor===c.value?r.selected:""}`,children:(0,m.jsx)("div",{className:`${r.colorOption} ${N.annotationColor===c.value?r.selected:""}`,style:{backgroundColor:c.value},title:c.label})},c.value))})]}),(0,m.jsxs)("div",{className:r.settingsSection,children:[(0,m.jsxs)("label",{className:r.settingsToggle,children:[(0,m.jsx)("input",{type:"checkbox",id:"autoClearAfterCopy",checked:N.autoClearAfterCopy,onChange:c=>Bn(d=>({...d,autoClearAfterCopy:c.target.checked}))}),(0,m.jsx)("label",{className:`${r.customCheckbox} ${N.autoClearAfterCopy?r.checked:""}`,htmlFor:"autoClearAfterCopy",children:N.autoClearAfterCopy&&(0,m.jsx)(s5,{size:14})}),(0,m.jsxs)("span",{className:`${r.toggleLabel} ${I?"":r.light}`,children:["Clear on copy/send",(0,m.jsx)($l,{content:"Automatically clear annotations after copying",children:(0,m.jsx)("span",{className:`${r.helpIcon} ${r.helpIconNudge2}`,children:(0,m.jsx)(Qa,{size:20})})})]})]}),(0,m.jsxs)("label",{className:`${r.settingsToggle} ${r.settingsToggleMarginBottom}`,children:[(0,m.jsx)("input",{type:"checkbox",id:"blockInteractions",checked:N.blockInteractions,onChange:c=>Bn(d=>({...d,blockInteractions:c.target.checked}))}),(0,m.jsx)("label",{className:`${r.customCheckbox} ${N.blockInteractions?r.checked:""}`,htmlFor:"blockInteractions",children:N.blockInteractions&&(0,m.jsx)(s5,{size:14})}),(0,m.jsx)("span",{className:`${r.toggleLabel} ${I?"":r.light}`,children:"Block page interactions"})]})]}),(0,m.jsx)("div",{className:`${r.settingsSection} ${r.settingsSectionExtraPadding}`,children:(0,m.jsxs)("button",{className:`${r.settingsNavLink} ${I?"":r.light}`,onClick:()=>hu("automations"),children:[(0,m.jsx)("span",{children:"Manage MCP & Webhooks"}),(0,m.jsxs)("span",{className:r.settingsNavLinkRight,children:[y&&lt!=="disconnected"&&(0,m.jsx)("span",{className:`${r.mcpNavIndicator} ${r[lt]}`}),(0,m.jsx)("svg",{width:"16",height:"16",viewBox:"0 0 16 16",fill:"none",xmlns:"http://www.w3.org/2000/svg",children:(0,m.jsx)("path",{d:"M7.5 12.5L12 8L7.5 3.5",stroke:"currentColor",strokeWidth:"1.5",strokeLinecap:"round",strokeLinejoin:"round"})})]})]})})]}),(0,m.jsxs)("div",{className:`${r.settingsPage} ${r.automationsPage} ${mu==="automations"?r.slideIn:""}`,children:[(0,m.jsxs)("button",{className:`${r.settingsBackButton} ${I?"":r.light}`,onClick:()=>hu("main"),children:[(0,m.jsx)(ug,{size:16}),(0,m.jsx)("span",{children:"Manage MCP & Webhooks"})]}),(0,m.jsxs)("div",{className:r.settingsSection,children:[(0,m.jsxs)("div",{className:r.settingsRow,children:[(0,m.jsxs)("span",{className:`${r.automationHeader} ${I?"":r.light}`,children:["MCP Connection",(0,m.jsx)($l,{content:"Connect via Model Context Protocol to let AI agents like Claude Code receive annotations in real-time.",children:(0,m.jsx)("span",{className:`${r.helpIcon} ${r.helpIconNudgeDown}`,children:(0,m.jsx)(Qa,{size:20})})})]}),y&&(0,m.jsx)("div",{className:`${r.mcpStatusDot} ${r[lt]}`,title:lt==="connected"?"Connected":lt==="connecting"?"Connecting...":"Disconnected"})]}),(0,m.jsxs)("p",{className:`${r.automationDescription} ${I?"":r.light}`,style:{paddingBottom:6},children:["MCP connection allows agents to receive and act on annotations."," ",(0,m.jsx)("a",{href:"https://agentation.dev/mcp",target:"_blank",rel:"noopener noreferrer",className:`${r.learnMoreLink} ${I?"":r.light}`,children:"Learn more"})]})]}),(0,m.jsxs)("div",{className:`${r.settingsSection} ${r.settingsSectionGrow}`,children:[(0,m.jsxs)("div",{className:r.settingsRow,children:[(0,m.jsxs)("span",{className:`${r.automationHeader} ${I?"":r.light}`,children:["Webhooks",(0,m.jsx)($l,{content:"Send annotation data to any URL endpoint when annotations change. Useful for custom integrations.",children:(0,m.jsx)("span",{className:`${r.helpIcon} ${r.helpIconNoNudge}`,children:(0,m.jsx)(Qa,{size:20})})})]}),(0,m.jsxs)("div",{className:r.autoSendRow,children:[(0,m.jsx)("span",{className:`${r.autoSendLabel} ${I?"":r.light} ${N.webhooksEnabled?r.active:""}`,children:"Auto-Send"}),(0,m.jsxs)("label",{className:`${r.toggleSwitch} ${N.webhookUrl?"":r.disabled}`,children:[(0,m.jsx)("input",{type:"checkbox",checked:N.webhooksEnabled,disabled:!N.webhookUrl,onChange:()=>Bn(c=>({...c,webhooksEnabled:!c.webhooksEnabled}))}),(0,m.jsx)("span",{className:r.toggleSlider})]})]})]}),(0,m.jsx)("p",{className:`${r.automationDescription} ${I?"":r.light}`,children:"The webhook URL will receive live annotation changes and annotation data."}),(0,m.jsx)("textarea",{className:`${r.webhookUrlInput} ${I?"":r.light}`,placeholder:"Webhook URL",value:N.webhookUrl,style:{"--marker-color":N.annotationColor},onKeyDown:c=>c.stopPropagation(),onChange:c=>Bn(d=>({...d,webhookUrl:c.target.value}))})]})]})]})})]})}),(0,m.jsxs)("div",{className:r.markersLayer,"data-feedback-toolbar":!0,children:[$&&bi.filter(c=>!c.isFixed).map((c,d)=>{let C=!Be&&ri===c.id,T=Od===c.id,v=(C||T)&&!P,z=c.isMultiSelect,B=z?"#34C759":N.annotationColor,Y=f.findIndex(X=>X.id===c.id),V=!Fd.has(c.id),Q=Be?r.exit:zd?r.clearing:V?r.enter:"",R=v&&N.markerClickBehavior==="delete";return(0,m.jsxs)("div",{className:`${r.marker} ${z?r.multiSelect:""} ${Q} ${R?r.hovered:""}`,"data-annotation-marker":!0,style:{left:`${c.x}%`,top:c.y,backgroundColor:R?void 0:B,animationDelay:Be?`${(bi.length-1-d)*20}ms`:`${d*20}ms`},onMouseEnter:()=>!Be&&c.id!==hi.current&&pi(c),onMouseLeave:()=>pi(null),onClick:X=>{X.stopPropagation(),Be||(N.markerClickBehavior==="delete"?xu(c.id):gi(c))},onContextMenu:X=>{N.markerClickBehavior==="delete"&&(X.preventDefault(),X.stopPropagation(),Be||gi(c))},children:[v?R?(0,m.jsx)(dd,{size:z?18:16}):(0,m.jsx)(u5,{size:16}):(0,m.jsx)("span",{className:di!==null&&Y>=di?r.renumber:void 0,children:Y+1}),C&&!P&&(0,m.jsxs)("div",{className:`${r.markerTooltip} ${I?"":r.light} ${r.enter}`,style:r_(c),children:[(0,m.jsxs)("span",{className:r.markerQuote,children:[c.element,c.selectedText&&` "${c.selectedText.slice(0,30)}${c.selectedText.length>30?"...":""}"`]}),(0,m.jsx)("span",{className:r.markerNote,children:c.comment})]})]},c.id)}),$&&!Be&&c_.filter(c=>!c.isFixed).map(c=>{let d=c.isMultiSelect;return(0,m.jsx)("div",{className:`${r.marker} ${r.hovered} ${d?r.multiSelect:""} ${r.exit}`,"data-annotation-marker":!0,style:{left:`${c.x}%`,top:c.y},children:(0,m.jsx)(dd,{size:d?12:10})},c.id)})]}),(0,m.jsxs)("div",{className:r.fixedMarkersLayer,"data-feedback-toolbar":!0,children:[$&&bi.filter(c=>c.isFixed).map((c,d)=>{let C=bi.filter(K=>K.isFixed),T=!Be&&ri===c.id,v=Od===c.id,z=(T||v)&&!P,B=c.isMultiSelect,Y=B?"#34C759":N.annotationColor,V=f.findIndex(K=>K.id===c.id),Q=!Fd.has(c.id),R=Be?r.exit:zd?r.clearing:Q?r.enter:"",X=z&&N.markerClickBehavior==="delete";return(0,m.jsxs)("div",{className:`${r.marker} ${r.fixed} ${B?r.multiSelect:""} ${R} ${X?r.hovered:""}`,"data-annotation-marker":!0,style:{left:`${c.x}%`,top:c.y,backgroundColor:X?void 0:Y,animationDelay:Be?`${(C.length-1-d)*20}ms`:`${d*20}ms`},onMouseEnter:()=>!Be&&c.id!==hi.current&&pi(c),onMouseLeave:()=>pi(null),onClick:K=>{K.stopPropagation(),Be||(N.markerClickBehavior==="delete"?xu(c.id):gi(c))},onContextMenu:K=>{N.markerClickBehavior==="delete"&&(K.preventDefault(),K.stopPropagation(),Be||gi(c))},children:[z?X?(0,m.jsx)(dd,{size:B?18:16}):(0,m.jsx)(u5,{size:16}):(0,m.jsx)("span",{className:di!==null&&V>=di?r.renumber:void 0,children:V+1}),T&&!P&&(0,m.jsxs)("div",{className:`${r.markerTooltip} ${I?"":r.light} ${r.enter}`,style:r_(c),children:[(0,m.jsxs)("span",{className:r.markerQuote,children:[c.element,c.selectedText&&` "${c.selectedText.slice(0,30)}${c.selectedText.length>30?"...":""}"`]}),(0,m.jsx)("span",{className:r.markerNote,children:c.comment})]})]},c.id)}),$&&!Be&&c_.filter(c=>c.isFixed).map(c=>{let d=c.isMultiSelect;return(0,m.jsx)("div",{className:`${r.marker} ${r.fixed} ${r.hovered} ${d?r.multiSelect:""} ${r.exit}`,"data-annotation-marker":!0,style:{left:`${c.x}%`,top:c.y},children:(0,m.jsx)(Jy,{size:d?12:10})},c.id)})]}),k&&(0,m.jsxs)("div",{className:r.overlay,"data-feedback-toolbar":!0,style:D||P?{zIndex:99999}:void 0,children:[pt?.rect&&!D&&!Rd&&!dn&&(0,m.jsx)("div",{className:`${r.hoverHighlight} ${r.enter}`,style:{left:pt.rect.left,top:pt.rect.top,width:pt.rect.width,height:pt.rect.height,borderColor:`${N.annotationColor}80`,backgroundColor:`${N.annotationColor}0A`}}),Ye.filter(c=>document.contains(c.element)).map((c,d)=>{let C=c.element.getBoundingClientRect(),T=Ye.length>1;return(0,m.jsx)("div",{className:T?r.multiSelectOutline:r.singleSelectOutline,style:{position:"fixed",left:C.left,top:C.top,width:C.width,height:C.height,...T?{}:{borderColor:`${N.annotationColor}99`,backgroundColor:`${N.annotationColor}0D`}}},d)}),ri&&!D&&(()=>{let c=f.find(v=>v.id===ri);if(!c?.boundingBox)return null;if(c.elementBoundingBoxes?.length)return Ld.length>0?Ld.filter(v=>document.contains(v)).map((v,z)=>{let B=v.getBoundingClientRect();return(0,m.jsx)("div",{className:`${r.multiSelectOutline} ${r.enter}`,style:{left:B.left,top:B.top,width:B.width,height:B.height}},`hover-outline-live-${z}`)}):c.elementBoundingBoxes.map((v,z)=>(0,m.jsx)("div",{className:`${r.multiSelectOutline} ${r.enter}`,style:{left:v.x,top:v.y-yl,width:v.width,height:v.height}},`hover-outline-${z}`));let d=du&&document.contains(du)?du.getBoundingClientRect():null,C=d?{x:d.left,y:d.top,width:d.width,height:d.height}:{x:c.boundingBox.x,y:c.isFixed?c.boundingBox.y:c.boundingBox.y-yl,width:c.boundingBox.width,height:c.boundingBox.height},T=c.isMultiSelect;return(0,m.jsx)("div",{className:`${T?r.multiSelectOutline:r.singleSelectOutline} ${r.enter}`,style:{left:C.x,top:C.y,width:C.width,height:C.height,...T?{}:{borderColor:`${N.annotationColor}99`,backgroundColor:`${N.annotationColor}0D`}}})})(),pt&&!D&&!Rd&&!dn&&(0,m.jsxs)("div",{className:`${r.hoverTooltip} ${r.enter}`,style:{left:Math.max(8,Math.min(Xl.x,window.innerWidth-100)),top:Math.max(Xl.y-(pt.reactComponents?48:32),8)},children:[pt.reactComponents&&(0,m.jsx)("div",{className:r.hoverReactPath,children:pt.reactComponents}),(0,m.jsx)("div",{className:r.hoverElementName,children:pt.elementName})]}),D&&(0,m.jsxs)(m.Fragment,{children:[D.multiSelectElements?.length?D.multiSelectElements.filter(c=>document.contains(c)).map((c,d)=>{let C=c.getBoundingClientRect();return(0,m.jsx)("div",{className:`${r.multiSelectOutline} ${Wa?r.exit:r.enter}`,style:{left:C.left,top:C.top,width:C.width,height:C.height}},`pending-multi-${d}`)}):D.targetElement&&document.contains(D.targetElement)?(()=>{let c=D.targetElement.getBoundingClientRect();return(0,m.jsx)("div",{className:`${r.singleSelectOutline} ${Wa?r.exit:r.enter}`,style:{left:c.left,top:c.top,width:c.width,height:c.height,borderColor:`${N.annotationColor}99`,backgroundColor:`${N.annotationColor}0D`}})})():D.boundingBox&&(0,m.jsx)("div",{className:`${D.isMultiSelect?r.multiSelectOutline:r.singleSelectOutline} ${Wa?r.exit:r.enter}`,style:{left:D.boundingBox.x,top:D.boundingBox.y-yl,width:D.boundingBox.width,height:D.boundingBox.height,...D.isMultiSelect?{}:{borderColor:`${N.annotationColor}99`,backgroundColor:`${N.annotationColor}0D`}}}),(()=>{let c=D.x,d=D.isFixed?D.y:D.y-yl;return(0,m.jsxs)(m.Fragment,{children:[(0,m.jsx)("div",{className:`${r.marker} ${r.pending} ${D.isMultiSelect?r.multiSelect:""} ${Wa?r.exit:r.enter}`,style:{left:`${c}%`,top:d,backgroundColor:D.isMultiSelect?"#34C759":N.annotationColor},children:(0,m.jsx)(Wy,{size:12})}),(0,m.jsx)(r5,{ref:l_,element:D.element,selectedText:D.selectedText,computedStyles:D.computedStylesObj,placeholder:D.element==="Area selection"?"What should change in this area?":D.isMultiSelect?"Feedback for this group of elements...":"What should change?",onSubmit:U5,onCancel:j5,isExiting:Wa,lightMode:!I,accentColor:D.isMultiSelect?"#34C759":N.annotationColor,style:{left:Math.max(160,Math.min(window.innerWidth-160,c/100*window.innerWidth)),...d>window.innerHeight-290?{bottom:window.innerHeight-d+20}:{top:d+20}}})]})})()]}),P&&(0,m.jsxs)(m.Fragment,{children:[P.elementBoundingBoxes?.length?Hd.length>0?Hd.filter(c=>document.contains(c)).map((c,d)=>{let C=c.getBoundingClientRect();return(0,m.jsx)("div",{className:`${r.multiSelectOutline} ${r.enter}`,style:{left:C.left,top:C.top,width:C.width,height:C.height}},`edit-multi-live-${d}`)}):P.elementBoundingBoxes.map((c,d)=>(0,m.jsx)("div",{className:`${r.multiSelectOutline} ${r.enter}`,style:{left:c.x,top:c.y-yl,width:c.width,height:c.height}},`edit-multi-${d}`)):(()=>{let c=_u&&document.contains(_u)?_u.getBoundingClientRect():null,d=c?{x:c.left,y:c.top,width:c.width,height:c.height}:P.boundingBox?{x:P.boundingBox.x,y:P.isFixed?P.boundingBox.y:P.boundingBox.y-yl,width:P.boundingBox.width,height:P.boundingBox.height}:null;return d?(0,m.jsx)("div",{className:`${P.isMultiSelect?r.multiSelectOutline:r.singleSelectOutline} ${r.enter}`,style:{left:d.x,top:d.y,width:d.width,height:d.height,...P.isMultiSelect?{}:{borderColor:`${N.annotationColor}99`,backgroundColor:`${N.annotationColor}0D`}}}):null})(),(0,m.jsx)(r5,{ref:a_,element:P.element,selectedText:P.selectedText,computedStyles:bg(P.computedStyles),placeholder:"Edit your feedback...",initialValue:P.comment,submitLabel:"Save",onSubmit:X5,onCancel:Q5,onDelete:()=>xu(P.id),isExiting:H5,lightMode:!I,accentColor:P.isMultiSelect?"#34C759":N.annotationColor,style:(()=>{let c=P.isFixed?P.y:P.y-yl;return{left:Math.max(160,Math.min(window.innerWidth-160,P.x/100*window.innerWidth)),...c>window.innerHeight-290?{bottom:window.innerHeight-c+20}:{top:c+20}}})()})]}),dn&&(0,m.jsxs)(m.Fragment,{children:[(0,m.jsx)("div",{ref:Ia,className:r.dragSelection}),(0,m.jsx)("div",{ref:Fa,className:r.highlightsContainer})]})]})]}),document.body)}var kd="recatch-bulk-import-agentation-session-id",ci="http://localhost:4747";function Md(e,t){window.dispatchEvent(new CustomEvent(e,{detail:t}))}async function E5(e,t){try{await fetch(e,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)})}catch(n){console.warn("Agentation callback failed",n)}}function ep(){let e=(0,Dn.useMemo)(()=>window.localStorage.getItem(kd)||"",[]),[t,n]=(0,Dn.useState)(e);return(0,Dn.useEffect)(()=>{Md("agentation:session",{sessionId:t||null,endpoint:ci})},[t]),Dn.default.createElement(w5,{endpoint:ci,sessionId:t||void 0,onSessionCreated:l=>{window.localStorage.setItem(kd,l),n(l),Md("agentation:session",{sessionId:l,endpoint:ci}),E5("/api/agentation/session",{session_id:l,endpoint:ci,created_at:new Date().toISOString()})},onSubmit:(l,a)=>{let o={session_id:window.localStorage.getItem(kd)||t||"",endpoint:ci,output:l,annotations:a,created_at:new Date().toISOString(),url:window.location.href};Md("agentation:submit",o),E5("/api/agentation/submit",o)}})}function T5(){let e=document.getElementById("agentation-root");e||(e=document.createElement("div"),e.id="agentation-root",document.body.appendChild(e)),(0,k5.createRoot)(e).render(Dn.default.createElement(ep,null))}document.readyState==="loading"?document.addEventListener("DOMContentLoaded",T5,{once:!0}):T5();})();
/*! Bundled license information:

react/cjs/react.production.js:
  (**
   * @license React
   * react.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

scheduler/cjs/scheduler.production.js:
  (**
   * @license React
   * scheduler.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

react-dom/cjs/react-dom.production.js:
  (**
   * @license React
   * react-dom.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

react-dom/cjs/react-dom-client.production.js:
  (**
   * @license React
   * react-dom-client.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)

react/cjs/react-jsx-runtime.production.js:
  (**
   * @license React
   * react-jsx-runtime.production.js
   *
   * Copyright (c) Meta Platforms, Inc. and affiliates.
   *
   * This source code is licensed under the MIT license found in the
   * LICENSE file in the root directory of this source tree.
   *)
*/
