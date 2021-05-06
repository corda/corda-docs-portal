import CookiesEuBanner from './vendor/cookies-eu-banner';
import { googleAnalytics } from './vendor/googleanalytics';
import { docSearchInit } from './vendor/doc-search';

const docsearchLoad = (resolve, reject) => {
    const script = document.createElement('script');
    document.body.appendChild(script);
    script.onload = resolve;
    script.onerror = reject;
    script.async = true;
    script.src = "https://cdn.jsdelivr.net/npm/docsearch.js@2.6.3/dist/cdn/docsearch.min.js";
};

export class DocsiteCookies {
    constructor() {
        this.name = 'corda_cookie';
        this.cookiesAccepted = {
            set: true,
            necessary: true,
            preferences: false,
            statistics: false,
            marketing: false
        };
        this.form = document.querySelector('#cookie-consent-form');
        this.handleAllCookies();

        new CookiesEuBanner(() => {
            this.cookieBanner();
        }, true);
    }

    handleAllCookies() {
        const acceptButton = document.querySelector('#cookies-eu-accept');
        const allCookiesButton = document.querySelector('#cookies-eu-accept-all');

        allCookiesButton.addEventListener('click', e => {
            e.preventDefault();
            this.allowAllCookies(this.form);
            acceptButton.click();
        });
    }

    cookieBanner() {
        if (!this.checkConsent()) {
            this.formToCookie(this.name, this.form);
            this.setAdditionalServices();
        } else {
            this.setAdditionalServices();
        }
    }

    allowAllCookies(form) {
        let cookiePreferences = form.querySelectorAll('.cookies-checkbox');
        for (let cookie of cookiePreferences) {
            cookie.querySelector('input').checked = true;
        }
    }

    formToCookie(name, form) {
        const thirteenMonthsInMils = 31104000000;

        let date = new Date();
        date.setTime(date.getTime() + thirteenMonthsInMils);

        let formData = new FormData(form);
        for (var pair of formData.entries()) {
            switch (pair[0]) {
                case "necessary":
                    this.cookiesAccepted.necessary = (pair[1] === 'on') ?
                        true :
                        false;
                    break;
                case "preferences":
                    this.cookiesAccepted.preferences = (pair[1] === 'on') ?
                        true :
                        false;
                    break;
                case "statistics":
                    this.cookiesAccepted.statistics = (pair[1] === 'on') ?
                        true :
                        false;
                    break;
                case "marketing":
                    this.cookiesAccepted.marketing = (pair[1] === 'on') ?
                        true :
                        false;
                    break;
                default:
                    break;
            }
        }
        let cookieValue = JSON.stringify(this.cookiesAccepted);

        document.cookie = `${name}=${cookieValue};expires=${date.toGMTString()};path=/`;
    }

    checkConsent() {
        let cookieName = this.name;
        let cookieValue = this.getCookie(cookieName);

        if (cookieValue) {
            if (cookieValue.set === true) {
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    getCookie(name) {
        let value = "; " + document.cookie;
        let parts = value.split("; " + name + "=");
        let cValue = "";

        if (parts.length == 2) {
            cValue = parts.pop().split(";").shift();
        }

        if (hasJsonStructure(cValue)) {
            return JSON.parse(cValue);
        } else {
            return cValue;
        }
    }

    setAdditionalServices() {
        let cookieConsent = this.getCookie(this.name);
        for (let [key, value] of Object.entries(cookieConsent)) {
            if (key === 'necessary' && value === true) {
                new Promise(docsearchLoad)
                    .then(() => {
                        docSearchInit();
                    })
                    .catch(err => console.log(err));
            }
            if (key === 'statistics' && value === true) {
                googleAnalytics();
            }
        }
    }
}

function hasJsonStructure(str) {
    if (typeof str !== 'string') return false;
    try {
        const result = JSON.parse(str);
        const type = Object.prototype.toString.call(result);
        return type === '[object Object]' ||
            type === '[object Array]';
    } catch (err) {
        return false;
    }
}