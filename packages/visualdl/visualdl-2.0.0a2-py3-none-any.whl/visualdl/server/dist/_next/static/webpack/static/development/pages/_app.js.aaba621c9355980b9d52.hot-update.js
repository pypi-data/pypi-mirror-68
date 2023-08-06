webpackHotUpdate("static/development/pages/_app.js",{

/***/ "./components/Navbar.tsx":
/*!*******************************!*\
  !*** ./components/Navbar.tsx ***!
  \*******************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _utils_i18n__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ~/utils/i18n */ "./utils/i18n.ts");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "../../node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils_style__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ~/utils/style */ "./utils/style.ts");
/* harmony import */ var _components_Icon__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ~/components/Icon */ "./components/Icon.tsx");
/* harmony import */ var _components_Language__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ~/components/Language */ "./components/Language.tsx");
/* harmony import */ var _utils_event__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ~/utils/event */ "./utils/event.ts");
/* harmony import */ var lodash_intersection__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! lodash/intersection */ "../../node_modules/lodash/intersection.js");
/* harmony import */ var lodash_intersection__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(lodash_intersection__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! styled-components */ "../../node_modules/styled-components/dist/styled-components.browser.esm.js");
/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! next/router */ "../../node_modules/next/dist/client/router.js");
/* harmony import */ var next_router__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(next_router__WEBPACK_IMPORTED_MODULE_8__);
var _this = undefined,
    _jsxFileName = "/Users/Peter/Baidu/ai/PaddlePaddle/VisualDL/frontend/packages/core/components/Navbar.tsx";

var __jsx = react__WEBPACK_IMPORTED_MODULE_1___default.a.createElement;









var buildNavItems = undefined;
var allNavItems = ['scalars', 'samples', 'graphs', 'high-dimensional'];
var navItems = buildNavItems ? lodash_intersection__WEBPACK_IMPORTED_MODULE_6___default()(buildNavItems.split(',').map(function (item) {
  return item.trim();
}), allNavItems) : allNavItems;
var Nav = styled_components__WEBPACK_IMPORTED_MODULE_7__["default"].nav.withConfig({
  displayName: "Navbar__Nav",
  componentId: "sc-1wmheaz-0"
})(["background-color:", ";color:", ";", " padding:0 ", ";display:flex;justify-content:space-between;align-items:stretch;> .left{display:flex;justify-content:flex-start;align-items:center;}> .right{display:flex;justify-content:flex-end;align-items:center;margin-right:-", ";}"], _utils_style__WEBPACK_IMPORTED_MODULE_2__["navbarBackgroundColor"], _utils_style__WEBPACK_IMPORTED_MODULE_2__["textInvertColor"], Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["size"])('100%'), Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(20), Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(20));
var Logo = styled_components__WEBPACK_IMPORTED_MODULE_7__["default"].a.withConfig({
  displayName: "Navbar__Logo",
  componentId: "sc-1wmheaz-1"
})(["font-size:", ";font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol';font-weight:600;margin-right:", ";> img{", " vertical-align:middle;margin-right:", ";}> span{vertical-align:middle;}"], Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(20), Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(40), Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["size"])(Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(31), Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(98)), Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(8));
var NavItem = styled_components__WEBPACK_IMPORTED_MODULE_7__["default"].a.withConfig({
  displayName: "Navbar__NavItem",
  componentId: "sc-1wmheaz-2"
})(["padding:0 ", ";height:100%;display:inline-flex;justify-content:center;align-items:center;background-color:", ";cursor:pointer;", " &:hover{background-color:", ";}> .nav-text{padding:", " 0 ", ";", " ", " text-transform:uppercase;}"], Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(20), _utils_style__WEBPACK_IMPORTED_MODULE_2__["navbarBackgroundColor"], Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["transitionProps"])('background-color'), _utils_style__WEBPACK_IMPORTED_MODULE_2__["navbarHoverBackgroundColor"], Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(10), Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(7), function (props) {
  return Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["border"])('bottom', Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["rem"])(3), 'solid', props.active ? _utils_style__WEBPACK_IMPORTED_MODULE_2__["navbarHighlightColor"] : 'transparent');
}, Object(_utils_style__WEBPACK_IMPORTED_MODULE_2__["transitionProps"])('border-bottom'));

var changeLanguage = function changeLanguage() {
  var language = _utils_i18n__WEBPACK_IMPORTED_MODULE_0__["i18n"].language;
  var allLanguages = _utils_i18n__WEBPACK_IMPORTED_MODULE_0__["config"].allLanguages;
  var index = allLanguages.indexOf(language);
  var nextLanguage = index < 0 || index >= allLanguages.length - 1 ? allLanguages[0] : allLanguages[index + 1];
  _utils_i18n__WEBPACK_IMPORTED_MODULE_0__["i18n"].changeLanguage(nextLanguage);
};

var Navbar = function Navbar() {
  var _useTranslation = Object(_utils_i18n__WEBPACK_IMPORTED_MODULE_0__["useTranslation"])('common'),
      t = _useTranslation.t,
      i18n = _useTranslation.i18n;

  var _useRouter = Object(next_router__WEBPACK_IMPORTED_MODULE_8__["useRouter"])(),
      pathname = _useRouter.pathname;

  var indexUrl = Object(react__WEBPACK_IMPORTED_MODULE_1__["useMemo"])(function () {
    var _localeSubpaths, _process$env$PUBLIC_P;

    // TODO: fix type
    var subpath = (_localeSubpaths = i18n.options.localeSubpaths) === null || _localeSubpaths === void 0 ? void 0 : _localeSubpaths[i18n.language];
    var path = (_process$env$PUBLIC_P = "") !== null && _process$env$PUBLIC_P !== void 0 ? _process$env$PUBLIC_P : '';

    if (subpath) {
      path += "/".concat(subpath);
    }

    return "".concat(path, "/index");
  }, [i18n]);
  return __jsx(Nav, {
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 117,
      columnNumber: 9
    }
  }, __jsx("div", {
    className: "left",
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 118,
      columnNumber: 13
    }
  }, __jsx(Logo, {
    href: indexUrl,
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 119,
      columnNumber: 17
    }
  }, __jsx("img", {
    alt: "PaddlePaddle",
    src: "".concat("", "/images/logo.svg"),
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 120,
      columnNumber: 21
    }
  }), __jsx("span", {
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 121,
      columnNumber: 21
    }
  }, "VisualDL")), navItems.map(function (name) {
    var href = "/".concat(name);
    return (// https://nextjs.org/docs/api-reference/next/link#if-the-child-is-a-custom-component-that-wraps-an-a-tag
      __jsx(_utils_i18n__WEBPACK_IMPORTED_MODULE_0__["Link"], {
        href: href,
        key: name,
        passHref: true,
        __self: _this,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 127,
          columnNumber: 25
        }
      }, __jsx(NavItem, {
        active: pathname === href,
        __self: _this,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 128,
          columnNumber: 29
        }
      }, __jsx("span", {
        className: "nav-text",
        __self: _this,
        __source: {
          fileName: _jsxFileName,
          lineNumber: 129,
          columnNumber: 33
        }
      }, t(name))))
    );
  })), __jsx("div", {
    className: "right",
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 135,
      columnNumber: 13
    }
  }, __jsx(NavItem, {
    onClick: changeLanguage,
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 136,
      columnNumber: 17
    }
  }, __jsx(_components_Language__WEBPACK_IMPORTED_MODULE_4__["default"], {
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 137,
      columnNumber: 21
    }
  })), __jsx(NavItem, {
    onClick: function onClick() {
      return _utils_event__WEBPACK_IMPORTED_MODULE_5__["default"].emit('refresh-running');
    },
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 139,
      columnNumber: 17
    }
  }, __jsx(_components_Icon__WEBPACK_IMPORTED_MODULE_3__["default"], {
    type: "refresh",
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 140,
      columnNumber: 21
    }
  }))));
};

/* harmony default export */ __webpack_exports__["default"] = (Navbar);

/***/ })

})
//# sourceMappingURL=_app.js.aaba621c9355980b9d52.hot-update.js.map