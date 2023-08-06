webpackHotUpdate("static/development/pages/high-dimensional.js",{

/***/ "./components/ScatterChart.tsx":
/*!*************************************!*\
  !*** ./components/ScatterChart.tsx ***!
  \*************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _babel_runtime_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @babel/runtime/helpers/esm/defineProperty */ "../../node_modules/@babel/runtime/helpers/esm/defineProperty.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "../../node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "../../node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _utils_style__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ~/utils/style */ "./utils/style.ts");
/* harmony import */ var react_spinners_GridLoader__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react-spinners/GridLoader */ "../../node_modules/react-spinners/GridLoader.js");
/* harmony import */ var react_spinners_GridLoader__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react_spinners_GridLoader__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! styled-components */ "../../node_modules/styled-components/dist/styled-components.browser.esm.js");
/* harmony import */ var _hooks_useECharts__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ~/hooks/useECharts */ "./hooks/useECharts.ts");



var _this = undefined,
    _jsxFileName = "/Users/Peter/Baidu/ai/PaddlePaddle/VisualDL/frontend/packages/core/components/ScatterChart.tsx";

var __jsx = react__WEBPACK_IMPORTED_MODULE_2___default.a.createElement;

function ownKeys(object, enumerableOnly) { var keys = Object.keys(object); if (Object.getOwnPropertySymbols) { var symbols = Object.getOwnPropertySymbols(object); if (enumerableOnly) symbols = symbols.filter(function (sym) { return Object.getOwnPropertyDescriptor(object, sym).enumerable; }); keys.push.apply(keys, symbols); } return keys; }

function _objectSpread(target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i] != null ? arguments[i] : {}; if (i % 2) { ownKeys(Object(source), true).forEach(function (key) { Object(_babel_runtime_helpers_esm_defineProperty__WEBPACK_IMPORTED_MODULE_0__["default"])(target, key, source[key]); }); } else if (Object.getOwnPropertyDescriptors) { Object.defineProperties(target, Object.getOwnPropertyDescriptors(source)); } else { ownKeys(Object(source)).forEach(function (key) { Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key)); }); } } return target; }






var Wrapper = styled_components__WEBPACK_IMPORTED_MODULE_5__["default"].div.withConfig({
  displayName: "ScatterChart__Wrapper",
  componentId: "nafbih-0"
})(["position:relative;background-color:", ";> .echarts{height:100%;}> .loading{", " ", " display:flex;justify-content:center;align-items:center;}"], _utils_style__WEBPACK_IMPORTED_MODULE_3__["backgroundColor"], Object(_utils_style__WEBPACK_IMPORTED_MODULE_3__["position"])('absolute', 0, null, null, 0), Object(_utils_style__WEBPACK_IMPORTED_MODULE_3__["size"])('100%'));
var SYMBOL_SIZE = 12;
var options2D = {
  xAxis: {},
  yAxis: {},
  toolbox: {
    show: true,
    showTitle: false,
    itemSize: 0,
    feature: {
      dataZoom: {},
      restore: {},
      saveAsImage: {}
    }
  }
};
var options3D = {
  grid3D: {},
  xAxis3D: {},
  yAxis3D: {},
  zAxis3D: {}
};
var series2D = {
  symbolSize: SYMBOL_SIZE,
  type: 'scatter'
};
var series3D = {
  symbolSize: SYMBOL_SIZE,
  type: 'scatter3D'
};

var ScatterChart = function ScatterChart(_ref) {
  var data = _ref.data,
      loading = _ref.loading,
      gl = _ref.gl,
      className = _ref.className;

  var _useECharts = Object(_hooks_useECharts__WEBPACK_IMPORTED_MODULE_6__["default"])({
    loading: loading,
    gl: gl
  }),
      ref = _useECharts.ref,
      echart = _useECharts.echart;

  var chartOptions = Object(react__WEBPACK_IMPORTED_MODULE_2__["useMemo"])(function () {
    var _data$map;

    return _objectSpread({}, gl ? options3D : options2D, {
      series: (_data$map = data === null || data === void 0 ? void 0 : data.map(function (series) {
        return _objectSpread({}, gl ? series3D : series2D, {}, series);
      })) !== null && _data$map !== void 0 ? _data$map : []
    });
  }, [gl, data]);
  Object(react__WEBPACK_IMPORTED_MODULE_2__["useEffect"])(function () {
    if (true) {
      var _echart$current;

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      echart === null || echart === void 0 ? void 0 : (_echart$current = echart.current) === null || _echart$current === void 0 ? void 0 : _echart$current.setOption(chartOptions, {
        notMerge: true
      });
    }
  }, [chartOptions, echart]);
  return __jsx(Wrapper, {
    className: className,
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 93,
      columnNumber: 9
    }
  }, !echart && __jsx("div", {
    className: "loading",
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 95,
      columnNumber: 17
    }
  }, __jsx(react_spinners_GridLoader__WEBPACK_IMPORTED_MODULE_4___default.a, {
    color: _utils_style__WEBPACK_IMPORTED_MODULE_3__["primaryColor"],
    size: "10px",
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 96,
      columnNumber: 21
    }
  })), __jsx("div", {
    className: "echarts",
    ref: ref,
    __self: _this,
    __source: {
      fileName: _jsxFileName,
      lineNumber: 99,
      columnNumber: 13
    }
  }));
};

ScatterChart.propTypes = {
  loading: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool,
  data: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array,
  gl: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.bool
};
/* harmony default export */ __webpack_exports__["default"] = (ScatterChart);

/***/ })

})
//# sourceMappingURL=high-dimensional.js.de8f44bd0e43fc0895f4.hot-update.js.map