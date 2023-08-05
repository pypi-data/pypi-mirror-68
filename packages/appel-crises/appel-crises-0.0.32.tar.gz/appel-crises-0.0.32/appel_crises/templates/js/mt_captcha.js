var isSignatureCaptchaValid = false;
var isCallOutCaptchaValid = false;
function mt_verifiedcb(state) {
    if (state.domID === 'mtcaptcha-1'){
        isSignatureCaptchaValid = true;
        onSignatureFormInput();
    }
    if (state.domID === 'mtcaptcha-2'){
        isCallOutCaptchaValid = true;
        onCallOutFormInput();
    }
}
function mt_verifyexpiredcb(state) {
    if (state.domID === 'mtcaptcha-1'){
        isSignatureCaptchaValid = false;
        onSignatureFormInput();
    }
    if (state.domID === 'mtcaptcha-2'){
        isCallOutCaptchaValid = false;
        onCallOutFormInput();
    }

}
function mt_errorcb(state) {
    if (state.domID === 'mtcaptcha-1'){
        isSignatureCaptchaValid = false;
        onSignatureFormInput();
    }
    if (state.domID === 'mtcaptcha-2'){
        isCallOutCaptchaValid = false;
        onCallOutFormInput();
    }

}

function mt_loaded_cb() {
    mtCaptchaHasLoaded = true;
}

var mtcaptchaConfig = {
    "sitekey": "MTPublic-trlyecjLJ",
    "autoFormValidate": true,
    "renderQueue": ['mtcaptcha-1', 'mtcaptcha-2'],
    "lang": "fr",
    "customLangText": {
        "fr": {
            "emptyCaptcha": "S'il vous plaît, complétez le défi CAPTCHA"
        }
    },
    "verified-callback": "mt_verifiedcb",
    "verifyexpired-callback": "mt_verifyexpiredcb",
    "error-callback": "mt_errorcb",
    "jsloaded-callback": "mt_loaded_cb",
};
(function () {
    var mt_service = document.createElement('script');
    mt_service.async = true;
    mt_service.src = 'https://service.mtcaptcha.com/mtcv1/client/mtcaptcha.min.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(mt_service);
    var mt_service2 = document.createElement('script');
    mt_service2.async = true;
    mt_service2.src = 'https://service2.mtcaptcha.com/mtcv1/client/mtcaptcha2.min.js';
    (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(mt_service2);
})();
