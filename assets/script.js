/** EMAIL REVEAL */
function reveal_email() {
    translations['es']['email_addr'] = 'contacto';
    translations['en']['email_addr'] = 'hi';
    translate(curr_lang());
}

/** TRANSLATION **/
import { EN, ES } from './strings.js';
const translations = {
    'en': EN,
    'es': ES
}, DEBUG = false;
const HTML_HARDCODED_LANG = 'es';
function curr_lang() {
    return document.documentElement.lang;
}
let callbackActiveFilter = null;
function translate(lang = 'en') {
    let first = translations[HTML_HARDCODED_LANG] === null;
    if (first)
        translations[HTML_HARDCODED_LANG] = {
            'description': document.querySelector('meta[name="description"]').getAttribute("content")
        };
    lang = lang.substring(0, 2).toLowerCase();
    if (translations[lang] === undefined)
        return;
    document.documentElement.lang = lang;
    let strings = translations[lang],
        list_translate = document.querySelectorAll('[data-string]');
    document.querySelector('meta[name="description"]').setAttribute("content", strings['description']);
    document.getElementById('lang-switch').checked = lang !== 'es';
    for (let i=0; i < list_translate.length; i++) {
        let elem_translate = list_translate[i],
            string_name = elem_translate.getAttribute("data-string");
        if (first)
            translations[HTML_HARDCODED_LANG][string_name] = elem_translate.innerHTML;
        if (strings[string_name] !== undefined)
            elem_translate.innerHTML = strings[string_name];
        else if (DEBUG)
            console.log("Translation not found for " + string_name)
    }
    const email_revealed = !strings['email_addr'].includes('*');
    document.querySelectorAll('.mailto_link').forEach(elem => {
        if (email_revealed) {
            if (!elem.hasAttribute('href')) {
                setTimeout(() => {
                    elem.href = 'mailto:' + strings['email_addr'] + '@jorgebruned.com';
                    elem.target = '_blank';
                    elem.onclick = null;
                    const tooltip = bootstrap.Tooltip.getOrCreateInstance(elem);
                    tooltip.hide();
                    elem.setAttribute('data-bs-original-title', 'Send me an email');
                }, 50); // Delay 50ms
            } else {   
                elem.href = 'mailto:' + strings['email_addr'] + '@jorgebruned.com';
            }
        } else {
            elem.removeAttribute('href');
            elem.onclick = reveal_email;
            // Show pointer cursor
            elem.style.cursor = 'pointer';
            elem.title = 'Reveal email';
            elem.setAttribute('data-bs-toggle', 'tooltip');
            elem.setAttribute('data-bs-placement', 'bottom');
        }
    });
    if (callbackActiveFilter !== null)
        callbackActiveFilter();
}

/** ANIMATIONS **/
const THRESHOLD_SCROLL_ANIMATIONS = 20;
function is_visible (elem) {
    let scroll_top = $(window).scrollTop() - THRESHOLD_SCROLL_ANIMATIONS,
        scroll_bottom = scroll_top + $(window).outerHeight(),
        offset_top = $(elem).offset().top,
        offset_bottom = scroll_top + Math.floor($(elem).outerHeight());
    return (scroll_bottom >= offset_top && scroll_top <= offset_bottom);
}

/** INITIALIZE ELEMENTS AND LISTENERS **/
$(window).on("load", function() {
    // Get user language and translate
    document.getElementById('lang-switch').onchange = () => {
        translate(document.getElementById('lang-switch').checked ? 'en' : 'es');
    }
    const path_url = window.location.pathname,
          path_lang = path_url == "/es" || path_url == "/en" ? path_url.substring(1) : null,
          get_url = window.location.search || '',
          get_lang = get_url.indexOf("lang") > -1 ? get_url.split("lang")[1].substr(1) : null;
    translate(path_lang || get_lang || window.navigator.userLanguage || window.navigator.language);

    // Scroll animations (navbar and animate-*)
    let animated = Array.prototype.slice.call(document.querySelectorAll("[class*='animate-']")),
        know_bars = Array.prototype.slice.call(document.getElementsByClassName("bar-fill"));
    const navbar = document.getElementsByClassName('navbar-top')[0];
    const btn_scroll_top = document.getElementById('btn-scroll-top');

    function animate_on_scroll(animate_all = false) {
        // Animate navbar and toggle scroll top button
        let scroll_top = $(window).scrollTop();
        if (navbar) {
            if (scroll_top > 0 && navbar.classList.contains('navbar-top')) {
                navbar.classList.remove('navbar-top');
                btn_scroll_top.classList.remove('hidden-right');
            } else if (scroll_top === 0 && !navbar.classList.contains('navbar-top')) {
                navbar.classList.add('navbar-top');
                btn_scroll_top.classList.add('hidden-right');
            }
        }
        if (btn_scroll_top) {
            if (scroll_top > 0 && btn_scroll_top.classList.contains('hidden-right')) {
                btn_scroll_top.classList.remove('hidden-right');
            } else if (scroll_top === 0 && !btn_scroll_top.classList.contains('hidden-right')) {
                btn_scroll_top.classList.add('hidden-right');
            }
        }

        // Animate classes animate-*
        animated.forEach((elem, i) => {
            if (animate_all || is_visible(elem)) {
                $(elem).addClass('animated');
            }
        });
        animated = animated.filter(elem => !elem.classList.contains('animated'));

        // Animate knowledge bars
        know_bars.forEach((elem, i) => {
            if (animate_all || is_visible(elem)) {
                elem.style = 'width:' + elem.getAttribute('data-width');
            }
        });
        know_bars = know_bars.filter(elem => elem.style.width !== '0%');
    }

    // Animate when the user scrolls
    animate_on_scroll();
    $(window).scroll(() => {
        animate_on_scroll();
    });

    // Initialize Isotope JS (the current implementation only allows one filter group per page)
    const filter = $('.grid').isotope({
        itemSelector: '.grid-item',
        layoutMode: 'masonry',
        masonry: {
            columnWidth: '.grid-item-small'
        }
    }), indicator = document.getElementById("portfolio-tag-indicator");
    function moveIndicator(left, width) {
        indicator.style.left = left + "px";
        indicator.style.width = width + "px";
    }
    function setActiveFilter(elem = null) {
        let currActive = document.getElementsByClassName("portfolio-filter active")[0];
        if (currActive == null)
            currActive = document.getElementsByClassName("portfolio-filter")[0];
        if (elem === null)
            elem = currActive;
        if (elem == null)
            return;
        filter.isotope({ filter: elem.getAttribute('data-filter') });
        moveIndicator(elem.offsetLeft, elem.offsetWidth);
        if (currActive != null)
            currActive.classList.remove("active");
        elem.classList.add("active");
    }
    Array.prototype.slice.call(document.getElementsByClassName("portfolio-filter")).forEach(elem => {
        elem.onclick = () => { setActiveFilter(elem); }
    });

    // Handle initial selection if provided in URL
    function idify(url) {
        return url.replace(/-/g, '_');
    }
    const hash_url = window.location.hash.substr(1),
          filter_selected_url = document.querySelectorAll('.portfolio-filter[data-filter=".' + idify(hash_url) + '"]');
    if (filter_selected_url.length === 1)
        setActiveFilter(filter_selected_url[0]);
    else
        setActiveFilter();

    // Handle window resize and set callback for translation
    $(window).resize(() => {
        setActiveFilter();
    });
    callbackActiveFilter = setActiveFilter;

    // Modal fix and lazy load media on modal show
    function lazy_load(elem) {
        if (elem.getAttribute('data-lazy-src') == null)
            return;
        console.log("Lazy loading " + elem.getAttribute('data-lazy-src'));
        elem.src = elem.getAttribute('data-lazy-src');
        elem.removeAttribute('data-lazy-src');
    }
    $('.modal').on('show.bs.modal', function() {
        $(this).insertAfter($('body'));
        $(this).find('[data-lazy-src]').each(function() {
            lazy_load(this);
        });
    });

    // Run animations and reveal email on print
    window.onbeforeprint = () => {
        animate_on_scroll(true);
        reveal_email();
    };

    // Open project modal or apply print styles if needed
    if (hash_url === 'print') {
        $('head').append('<link rel="stylesheet" type="text/css" href="/assets/print.css">');
        window.onbeforeprint();
    } else {
        const modal = document.getElementById('portfolio-details-' + idify(hash_url));
        if (modal != null)
            $(modal).modal('show');
    }

    // Initialize tooltips
    [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]')).map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Lazy load images
    function hasParentWithClass(node, classname) {
        if (node == null)
            return false;
        if (node.classList && node.classList.contains(classname))
            return true;
        return hasParentWithClass(node.parentNode, classname);
    }
    document.querySelectorAll('[data-lazy-src]').forEach(elem => {
        if (!hasParentWithClass(elem, 'modal')) {
            lazy_load(elem);
        }
    });

    // Add full-screen link to images in .post-content
    document.querySelectorAll('.post-content img').forEach(elem => {
        // Put image inside a link
        const a = document.createElement('a');
        a.classList.add('img-full-screen');
        a.classList.add('media-container');
        a.href = elem.src;
        a.target = '_blank';
        a.appendChild(elem.cloneNode(true));
        // Replace image with link
        elem.parentNode.replaceChild(a, elem);
    });

    // Put iframes inside a div with class .iframe-container inside a .media-container
    document.querySelectorAll('.post-content iframe').forEach(elem => {
        // Put iframe inside the necessary divs
        const div = document.createElement('div');
        div.classList.add('iframe-container');
        const div2 = document.createElement('div');
        div2.classList.add('media-container');
        div.appendChild(elem.cloneNode(true));
        div2.appendChild(div);
        // Replace iframe with div
        elem.parentNode.replaceChild(div2, elem);
    });
});