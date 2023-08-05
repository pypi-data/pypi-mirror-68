// https://stackoverflow.com/a/33928558/3218806
function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
        return clipboardData.setData("Text", text);

    }
    else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        }
        catch (ex) {
            console.warn("Copy to clipboard failed.", ex);
            return false;
        }
        finally {
            document.body.removeChild(textarea);
        }
    }
}

// UI utils
function removeClass(element, removeClass) {
    var newClassName = "";
    var i;
    var classes = element.className.split(" ");
    for (i = 0; i < classes.length; i++) {
        if (classes[i] !== removeClass) {
            newClassName += classes[i] + " ";
        }
    }
    if (i > 0) {
        newClassName = newClassName.substr(0, newClassName.length - 1);
    }
    element.className = newClassName;
}

function addClass(element, newClass) {
    element.className += " " + newClass;
}

function hasClass(object, className) {
    if (!object.className) return false;
    return (object.className.search('(^|\\s)' + className + '(\\s|$)') !== -1);
}

function showElementsOfClass(className) {
    var elements = document.getElementsByClassName(className);

    [].forEach.call(elements, function (el) {
        el.style.display = 'initial';
        if (hasClass(el, 'is-flex')) {
            el.style.display = 'flex';
        }
    });
}

function hideElementsOfClass(className) {
    var elements = document.getElementsByClassName(className);

    [].forEach.call(elements, function (el) {
        el.style.display = 'none';
    });
}

function displayIfJsElements() {
    showElementsOfClass("display-if-js");
    hideElementsOfClass("remove-if-js");
}
function displayNoJsElements() {
    hideElementsOfClass("display-if-js");
    showElementsOfClass("remove-if-js");
}

// CSRF middleware

/**
 * @param {FormData} data
 * @param {XMLHttpRequest} request
 */
function getCSRFTokenThenSend(data, request) {
    var csrfToken = getCookie('csrftoken');
    if (csrfToken !== null) {
        request.setRequestHeader("X-CSRFToken", csrfToken);
        request.send(data);
    } else {
        var csrfRequest = new XMLHttpRequest();
        csrfRequest.open("GET", "/api/csrf");
        csrfRequest.onload = function () {
            if (csrfRequest.status === 200) {
                csrfToken = getCookie('csrftoken');
                request.setRequestHeader("X-CSRFToken", csrfToken);
                request.send(data);
            } else {
                console.error("CSRF request failed.")
            }
        };
        csrfRequest.send();
    }
}

// Cookie parsing
// Source: https://docs.djangoproject.com/en/3.0/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Decideur form handling

function showCallOutForm() {
    showElementsOfClass("display-call-out");
    hideElementsOfClass("hide-call-out");

    // pre-fill fields
    var fullName = ((firstname.value && (firstname.value + " ")) || "") + (surname.value || "");
    if (fullName) {
        callOutSender.value = callOutSender.value || fullName;
        document.getElementById(
            "mail-content"
        ).value = document.getElementById(
            "mail-content"
        ).value.replace("[Votre signature]", fullName);
    }
    if (email.value) {
        callOutEmail.value = callOutEmail.value || email.value || "";
    }
}

function hideCallOutForm() {
    showElementsOfClass("hide-call-out");
    hideElementsOfClass("display-call-out");
}

function toggleCallOutForm() {
    var isFormShown = callOutForm.style.display !== 'none';
    if (isFormShown) {
        hideCallOutForm();
    } else {
        showCallOutForm();
    }
}

/**
 * @param {XMLHttpRequest} request
 */
function processCallOutResult(request) {
    document.getElementById("call-out-container").style.display = "none";

    if (request.status === 200) {
        document.getElementById("call-out-success").style.display = "block";
    } else {
        document.getElementById("call-out-error").style.display = "block";
        document.getElementById("call-out-error-text").innerText = request.responseText;
        console.error('Process call out result', request.status, request.responseText);
    }
}

function retryCallOutForm() {
    // Invert operation done by processCallOutResult on error
    document.getElementById("call-out-container").style.display = "initial";
    document.getElementById("call-out-error").style.display = "none";
}

/**
 * @param {string} content
 * @param {string} tagId
 * @param {string} data
 */
function addTag(content, tagId, data) {
    var close = document.createElement("span");
    close.innerText = "x";
    close.className = "close";
    var add = document.createElement("span");
    add.innerText = "+";
    add.className = "add";

    var newTag = document.createElement("span");
    newTag.id = tagId;
    newTag.innerText = content;
    newTag.className = "mail-to-tag depute-tag";
    newTag.setAttribute("data-circonscription", data);

    var parent = document.getElementById("call-out-recipients");
    parent.appendChild(newTag);
    newTag.onclick = function() {toggleTag(newTag.id)};
    newTag.appendChild(close);
    newTag.appendChild(add);
}

/**
 * @param deputes
 */
function changeTags(deputes) {
    // Remove all existing tags
    var tags = document.getElementsByClassName("depute-tag");
    while (tags.length > 0) tags[0].parentNode.removeChild(tags[0]);

    // Add new tags
    // If there is only one depute, we display : "Julius Caesar (député)"
    // Else we display : "Julius Caesar (député circ. n° 4 du 93)"

    var depute_name;
    var id_circ;
    if (deputes.length === 1) {
        id_circ = deputes[0][4];
        depute_name = deputes[0][0];
        addTag(depute_name + " (député)", "recipient-" + id_circ, id_circ);

    } else {
        var num_circ;
        var num_dpt;
        var annotation;

        for (var i = 0; i < deputes.length; i++) {
            id_circ = deputes[i][4];
            depute_name = deputes[i][0];
            num_circ = id_circ.split(".")[0];
            num_dpt = id_circ.split(".")[1];
            annotation = " (député circ. n°"+ num_circ + " du " + num_dpt + ")";
            addTag(depute_name + annotation, "recipient-" + id_circ, id_circ);
        }
    }
}

function onPostalCodeInput(event) {
    var code = event.target.value;
    if (code.length === 5) {
        getDepute(code);
    }
}

/**
 * Make sure all email (fake or not) inputs are synchronized
 *
 * @param {Event} event
 */
function onEmailInput(event) {
    var value = event.target.value;
    formFakeInput.innerText = value;
    callOutEmail.value = value;
    email.value = value;
}

/**
 * @param {string} postal_code
 */
function getDepute(postal_code) {
    var request = new XMLHttpRequest();
    request.open('GET', "/api/search-depute?postal_code=" + postal_code);
    request.onload = function () {
        if (request.status === 200) {
            changeTags(JSON.parse(request.responseText));
        } else {
            console.error("Error loading depute ", request.status, request.responseText)
        }
    };
    request.send();
}

function getRecipients() {
    var result = [];
    var tags = document.getElementsByClassName("depute-tag");
    for (var i = 0; i < tags.length; i++) {
        if (!isTagDisabled(tags[i])) {
            result.push(tags[i].getAttribute("data-circonscription"));
        }
    }
    return result;
}

function isTagDisabled(element) {
    return element.className.indexOf('disabled') !== -1;
}

function sendMail() {
    if (!isCallOutFormValid() || !isCallOutCaptchaValid) {
        return;
    }
    var formData = new FormData(document.getElementById("call-out-form"));
    formData.append('send_to_government', isTagDisabled(document.getElementById('government-tag')) ? '0' : '1');
    formData.append('circonscription_numbers', getRecipients().join(','));

    var request = new XMLHttpRequest();
    request.open("POST", "/api/call-out-ajax");
    request.onload = function () {
        processCallOutResult(request)
    };

    getCSRFTokenThenSend(formData, request);
}

// Fetching email template
function insertEmailTemplate() {
    var templates = JSON.parse(document.getElementById('email-templates-data').textContent);
    var template = templates[Math.floor(Math.random() * templates.length)];

    document.getElementById("mail-content").value = template["content"];
    document.getElementById("mail-subject").textContent = template["subject"];
    document.getElementById("mail-template-id").value = template["template_id"];
}

function closeTag(tag) {
    addClass(tag, 'disabled');
}
function enableTag(tag){
    removeClass(tag, 'disabled');
}

function toggleTag(tagId) {
    var element = document.getElementById(tagId);
    if (isTagDisabled(element)) {
        enableTag(element)
    } else {
        closeTag(element);
    }
}

// Signature form handling
function doSendSignature(ev) {

    var formData = new FormData(ev.target);

    var request = new XMLHttpRequest();
    request.open("POST", "/api/sign-ajax");
    request.onload = function () {
        processSignResult(request)
    };

    getCSRFTokenThenSend(formData, request);
}

function sendSignature(ev) {
    ev.preventDefault();

    if (!isSignatureFormValid() || !isSignatureCaptchaValid) {
        return;
    }
    // check if newsletter checked
    var newsletter = document.getElementById('news-checkbox');
    if (!newsletter.checked) {
        newsletterModal.style.display = "flex";
        eventBackup = ev;
        return; /* form will be sent by newsletterModal closing*/
    }
    doSendSignature(ev);
}
function acceptReceiveNews() {
    var newsletter = document.getElementById('news-checkbox');
    newsletter.checked = true;
    doSendSignature(eventBackup);
    newsletterModal.style.display = "none";
}
function denyReceiveNews() {
    doSendSignature(eventBackup);
    newsletterModal.style.display = "none";
}
function capitalize(s) {
    return s && s[0].toUpperCase() + s.slice(1);
}

/**
 * @param {XMLHttpRequest} request
 */
function processSignResult(request) {
    document.getElementById("sign-form").style.display = "none";

    if (request.status === 200) {
        document.getElementById("signature-result").style.display = "initial";
    } else if (request.status === 400) {
        document.getElementById("signature-error").style.display = "initial";
        document.getElementById("signature-error-text").innerText = request.responseText;
    } else {
        console.error("Invalid signature form submission", request.status, request.responseText);
        document.getElementById("signature-error").style.display = "initial";
    }
}

function retrySignature() {
    document.getElementById("sign-form").style.display = "initial";
    document.getElementById("signature-error").style.display = "none";
}

function isSignatureFormValid() {
    // is mail valid?
    if (!email.value || email.value.indexOf("@") === -1 || email.value.indexOf(".") === -1) {
        return false;
    }
    return firstname.value && surname.value;
}

function onSignatureFormInput() {
    if (isSignatureFormValid()) {
        showElementsOfClass("sign-captcha");
        if (isSignatureCaptchaValid) {
            removeClass(signatureSubmitBtn, "is-disabled");
        } else {
            addClass(signatureSubmitBtn, "is-disabled");
        }
    } else {
        addClass(signatureSubmitBtn, "is-disabled");
        hideElementsOfClass("sign-captcha");
    }
}

function isCallOutFormValid() {
    return callOutSender.value && callOutEmail.value && callOutPostalCode.value;
}

function onCallOutFormInput() {
    if (isCallOutFormValid()) {
        /* hack because it had no height on iPhone6 */
        document.getElementById('mail-right-col').style.minHeight = '610px';
        showElementsOfClass("call-out-captcha");
        if (isCallOutCaptchaValid && callOutLegal.checked) {
            removeClass(callOutSubmitBtn, "is-disabled");
        } else {
            addClass(callOutSubmitBtn, "is-disabled");
        }
    } else {
        addClass(callOutSubmitBtn, "is-disabled");
        document.getElementById('mail-right-col').style.minHeight = '450px';
        hideElementsOfClass("call-out-captcha");
    }
}

function detectIfMtCaptchaIsWorking() {
    if (!mtCaptchaHasLoaded) {
        console.warn("Mt Captcha library has not loaded");
        displayNoJsElements();
    }
}

function multiLineSujectOnMobile() {
    if (window.innerWidth < 900) {
        document.getElementById("mail-subject").setAttribute("rows", "2");
    }
}

function socialNetworkPopup(network) {
    socialNetworkModal.style.display = 'flex';
    document.getElementById('social-network-name').innerHTML = capitalize(network);
    document.getElementById('social-network-link').href = socialNetworkToUrl[network];
}
function copyPostTextToClipBoard() {
    var copied = copyToClipboard(socialNetworkText);
    if (copied) {
        document.getElementById("text-copied").style.display = 'block';
    }
}

// Binding elements and functions

var firstname = document.getElementById("firstname");
var surname = document.getElementById("surname");
var email = document.getElementById("email");
var newCheckbox = document.getElementById("news-checkbox");
var signatureSubmitBtn = document.getElementById("submit-btn");

var callOutSender = document.getElementById("call-out-sender");
var callOutEmail = document.getElementById("call-out-from_email");
var callOutPostalCode = document.getElementById("call-out-postal_code");
var callOutLegal = document.getElementById("call-out-legal");
var callOutSubmitBtn = document.getElementById("call-out-submit");
var callOutForm = document.getElementById("call-out-form-container");

var mtCaptchaHasLoaded = false;
var formFakeInput = document.getElementById("from-fake-input");
var socialNetworkToUrl = {
    facebook: "https://www.facebook.com/",
    instagram: "https://instagram.com/",
    whatsapp: "https://www.whatsapp.com/",
};
var newsletterModal = document.getElementById("newsletter-popup");
var socialNetworkModal = document.getElementById("social-network-popup");
var eventBackup = null;
var socialNetworkText = "Je viens de signer l’Appel commun à la reconstruction, un appel citoyen pour interpeller les décideurs et demander à ce que les mesures de relance soient à la hauteur des enjeux sociaux, sanitaires et écologiques. Nous ne pouvons tout simplement pas refaire le monde d'hier, un monde trop vulnérable et qui ne pourra pas faire face aux catastrophes à venir ! \n\nIl faut être nombreux à soutenir l'Appel si nous voulons reconstruire un monde plus écologique, plus juste : signez vous aussi l'Appel, et partagez-le autour de vous pour que nous soyons entendus !\n\nhttps://www.appel-commun-reconstruction.org/";

firstname.oninput = onSignatureFormInput;
surname.oninput = onSignatureFormInput;
email.oninput = function (ev) { onEmailInput(ev); onSignatureFormInput(ev);};

callOutSender.oninput = onCallOutFormInput;
callOutEmail.oninput = function(ev){onEmailInput(ev); onCallOutFormInput()};
callOutPostalCode.oninput = function(ev){onPostalCodeInput(ev); onCallOutFormInput()};
callOutLegal.oninput = onCallOutFormInput;

document.getElementById("sign-form").onsubmit = sendSignature;

displayIfJsElements();
setTimeout(detectIfMtCaptchaIsWorking, 2000);
insertEmailTemplate();
multiLineSujectOnMobile();

Sentry.init({ dsn: 'https://8843708aac354abdac2dcb62526d7d83@o386416.ingest.sentry.io/5220704' });
