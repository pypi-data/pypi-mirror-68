/*! Select2 4.0.7 | https://github.com/select2/select2/blob/master/LICENSE.md */

(function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var e=jQuery.fn.select2.amd;return e.define("select2/i18n/he",[],function(){return{errorLoading:function(){return"שגיאה בטעינת התוצאות"},inputTooLong:function(e){var t=e.input.length-e.maximum,n="נא למחוק ";return t===1?n+="תו אחד":n+=t+" תווים",n},inputTooShort:function(e){var t=e.minimum-e.input.length,n="נא להכניס ";return t===1?n+="תו אחד":n+=t+" תווים",n+=" או יותר",n},loadingMore:function(){return"טוען תוצאות נוספות…"},maximumSelected:function(e){var t="באפשרותך לבחור עד ";return e.maximum===1?t+="פריט אחד":t+=e.maximum+" פריטים",t},noResults:function(){return"לא נמצאו תוצאות"},searching:function(){return"מחפש…"},removeAllItems:function(){return"הסר את כל הפריטים"}}}),{define:e.define,require:e.require}})();