/* *
 *
 *  (c) 2010-2020 Torstein Honsi
 *
 *  License: www.highcharts.com/license
 *
 *  !!!!!!! SOURCE GETS TRANSPILED BY TYPESCRIPT. EDIT TS FILE ONLY. !!!!!!!
 *
 * */
'use strict';
import H from '../parts/Globals.js';
/**
 * Result object of a map transformation.
 *
 * @interface Highcharts.MapCoordinateObject
 */ /**
* X coordinate on the map.
* @name Highcharts.MapCoordinateObject#x
* @type {number}
*/ /**
* Y coordinate on the map.
* @name Highcharts.MapCoordinateObject#y
* @type {number|null}
*/
/**
 * A latitude/longitude object.
 *
 * @interface Highcharts.MapLatLonObject
 */ /**
* The latitude.
* @name Highcharts.MapLatLonObject#lat
* @type {number}
*/ /**
* The longitude.
* @name Highcharts.MapLatLonObject#lon
* @type {number}
*/
import U from '../parts/Utilities.js';
var error = U.error, extend = U.extend, format = U.format, merge = U.merge, wrap = U.wrap;
import '../parts/Options.js';
import '../parts/Chart.js';
var Chart = H.Chart, win = H.win;
/* eslint-disable no-invalid-this, valid-jsdoc */
/**
 * Test for point in polygon. Polygon defined as array of [x,y] points.
 * @private
 */
function pointInPolygon(point, polygon) {
    var i, j, rel1, rel2, c = false, x = point.x, y = point.y;
    for (i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        rel1 = polygon[i][1] > y;
        rel2 = polygon[j][1] > y;
        if (rel1 !== rel2 &&
            (x < (polygon[j][0] -
                polygon[i][0]) * (y - polygon[i][1]) /
                (polygon[j][1] - polygon[i][1]) +
                polygon[i][0])) {
            c = !c;
        }
    }
    return c;
}
/**
 * Highmaps only. Get point from latitude and longitude using specified
 * transform definition.
 *
 * @requires modules/map
 *
 * @sample maps/series/latlon-transform/
 *         Use specific transformation for lat/lon
 *
 * @function Highcharts.Chart#transformFromLatLon
 *
 * @param {Highcharts.MapLatLonObject} latLon
 *        A latitude/longitude object.
 *
 * @param {*} transform
 *        The transform definition to use as explained in the
 *        {@link https://www.highcharts.com/docs/maps/latlon|documentation}.
 *
 * @return {Highcharts.MapCoordinateObject}
 *         An object with `x` and `y` properties.
 */
Chart.prototype.transformFromLatLon = function (latLon, transform) {
    /**
     * Allows to manually load the proj4 library from Highcharts options
     * instead of the `window`.
     * In case of loading the library from a `script` tag,
     * this option is not needed, it will be loaded from there by default.
     *
     * @type       {function}
     * @product    highmaps
     * @apioption  chart.proj4
     */
    var _a;
    var proj4 = (((_a = this.userOptions.chart) === null || _a === void 0 ? void 0 : _a.proj4) || win.proj4);
    if (!proj4) {
        error(21, false, this);
        return {
            x: 0,
            y: null
        };
    }
    var projected = proj4(transform.crs, [latLon.lon, latLon.lat]), cosAngle = transform.cosAngle ||
        (transform.rotation && Math.cos(transform.rotation)), sinAngle = transform.sinAngle ||
        (transform.rotation && Math.sin(transform.rotation)), rotated = transform.rotation ? [
        projected[0] * cosAngle + projected[1] * sinAngle,
        -projected[0] * sinAngle + projected[1] * cosAngle
    ] : projected;
    return {
        x: ((rotated[0] - (transform.xoffset || 0)) * (transform.scale || 1) +
            (transform.xpan || 0)) * (transform.jsonres || 1) +
            (transform.jsonmarginX || 0),
        y: (((transform.yoffset || 0) - rotated[1]) * (transform.scale || 1) +
            (transform.ypan || 0)) * (transform.jsonres || 1) -
            (transform.jsonmarginY || 0)
    };
};
/**
 * Highmaps only. Get latLon from point using specified transform definition.
 * The method returns an object with the numeric properties `lat` and `lon`.
 *
 * @requires modules/map
 *
 * @sample maps/series/latlon-transform/
 *         Use specific transformation for lat/lon
 *
 * @function Highcharts.Chart#transformToLatLon
 *
 * @param {Highcharts.Point|Highcharts.MapCoordinateObject} point
 *        A `Point` instance, or any object containing the properties `x` and
 *        `y` with numeric values.
 *
 * @param {*} transform
 *        The transform definition to use as explained in the
 *        {@link https://www.highcharts.com/docs/maps/latlon|documentation}.
 *
 * @return {Highcharts.MapLatLonObject|undefined}
 *         An object with `lat` and `lon` properties.
 */
Chart.prototype.transformToLatLon = function (point, transform) {
    if (typeof win.proj4 === 'undefined') {
        error(21, false, this);
        return;
    }
    var normalized = {
        x: ((point.x -
            (transform.jsonmarginX || 0)) / (transform.jsonres || 1) -
            (transform.xpan || 0)) / (transform.scale || 1) +
            (transform.xoffset || 0),
        y: ((-point.y - (transform.jsonmarginY || 0)) / (transform.jsonres || 1) +
            (transform.ypan || 0)) / (transform.scale || 1) +
            (transform.yoffset || 0)
    }, cosAngle = transform.cosAngle ||
        (transform.rotation && Math.cos(transform.rotation)), sinAngle = transform.sinAngle ||
        (transform.rotation && Math.sin(transform.rotation)), 
    // Note: Inverted sinAngle to reverse rotation direction
    projected = win.proj4(transform.crs, 'WGS84', transform.rotation ? {
        x: normalized.x * cosAngle + normalized.y * -sinAngle,
        y: normalized.x * sinAngle + normalized.y * cosAngle
    } : normalized);
    return { lat: projected.y, lon: projected.x };
};
/**
 * Highmaps only. Calculate latitude/longitude values for a point. Returns an
 * object with the numeric properties `lat` and `lon`.
 *
 * @requires modules/map
 *
 * @sample maps/demo/latlon-advanced/
 *         Advanced lat/lon demo
 *
 * @function Highcharts.Chart#fromPointToLatLon
 *
 * @param {Highcharts.Point|Highcharts.MapCoordinateObject} point
 *        A `Point` instance or anything containing `x` and `y` properties with
 *        numeric values.
 *
 * @return {Highcharts.MapLatLonObject|undefined}
 *         An object with `lat` and `lon` properties.
 */
Chart.prototype.fromPointToLatLon = function (point) {
    var transforms = this.mapTransforms, transform;
    if (!transforms) {
        error(22, false, this);
        return;
    }
    for (transform in transforms) {
        if (Object.hasOwnProperty.call(transforms, transform) &&
            transforms[transform].hitZone &&
            pointInPolygon({ x: point.x, y: -point.y }, transforms[transform].hitZone.coordinates[0])) {
            return this.transformToLatLon(point, transforms[transform]);
        }
    }
    return this.transformToLatLon(point, transforms['default'] // eslint-disable-line dot-notation
    );
};
/**
 * Highmaps only. Get chart coordinates from latitude/longitude. Returns an
 * object with x and y values corresponding to the `xAxis` and `yAxis`.
 *
 * @requires modules/map
 *
 * @sample maps/series/latlon-to-point/
 *         Find a point from lat/lon
 *
 * @function Highcharts.Chart#fromLatLonToPoint
 *
 * @param {Highcharts.MapLatLonObject} latLon
 *        Coordinates.
 *
 * @return {Highcharts.MapCoordinateObject}
 *         X and Y coordinates in terms of chart axis values.
 */
Chart.prototype.fromLatLonToPoint = function (latLon) {
    var transforms = this.mapTransforms, transform, coords;
    if (!transforms) {
        error(22, false, this);
        return {
            x: 0,
            y: null
        };
    }
    for (transform in transforms) {
        if (Object.hasOwnProperty.call(transforms, transform) &&
            transforms[transform].hitZone) {
            coords = this.transformFromLatLon(latLon, transforms[transform]);
            if (pointInPolygon({ x: coords.x, y: -coords.y }, transforms[transform].hitZone.coordinates[0])) {
                return coords;
            }
        }
    }
    return this.transformFromLatLon(latLon, transforms['default'] // eslint-disable-line dot-notation
    );
};
/**
 * Highmaps only. Restructure a GeoJSON object in preparation to be read
 * directly by the
 * {@link https://api.highcharts.com/highmaps/plotOptions.series.mapData|series.mapData}
 * option. The GeoJSON will be broken down to fit a specific Highcharts type,
 * either `map`, `mapline` or `mappoint`. Meta data in GeoJSON's properties
 * object will be copied directly over to {@link Point.properties} in Highmaps.
 *
 * @requires modules/map
 *
 * @sample maps/demo/geojson/
 *         Simple areas
 * @sample maps/demo/geojson-multiple-types/
 *         Multiple types
 *
 * @function Highcharts.geojson
 *
 * @param {*} geojson
 *        The GeoJSON structure to parse, represented as a JavaScript object
 *        rather than a JSON string.
 *
 * @param {string} [hType=map]
 *        The Highmaps series type to prepare for. Setting "map" will return
 *        GeoJSON polygons and multipolygons. Setting "mapline" will return
 *        GeoJSON linestrings and multilinestrings. Setting "mappoint" will
 *        return GeoJSON points and multipoints.
 *
 * @return {Array<*>}
 *         An object ready for the `mapData` option.
 */
H.geojson = function (geojson, hType, series) {
    var mapData = [], path = [], polygonToPath = function (polygon) {
        var i, len = polygon.length;
        path.push('M');
        for (i = 0; i < len; i++) {
            if (i === 1) {
                path.push('L');
            }
            path.push(polygon[i][0], -polygon[i][1]);
        }
    };
    hType = hType || 'map';
    geojson.features.forEach(function (feature) {
        var geometry = feature.geometry, type = geometry.type, coordinates = geometry.coordinates, properties = feature.properties, point;
        path = [];
        if (hType === 'map' || hType === 'mapbubble') {
            if (type === 'Polygon') {
                coordinates.forEach(polygonToPath);
                path.push('Z');
            }
            else if (type === 'MultiPolygon') {
                coordinates.forEach(function (items) {
                    items.forEach(polygonToPath);
                });
                path.push('Z');
            }
            if (path.length) {
                point = { path: path };
            }
        }
        else if (hType === 'mapline') {
            if (type === 'LineString') {
                polygonToPath(coordinates);
            }
            else if (type === 'MultiLineString') {
                coordinates.forEach(polygonToPath);
            }
            if (path.length) {
                point = { path: path };
            }
        }
        else if (hType === 'mappoint') {
            if (type === 'Point') {
                point = {
                    x: coordinates[0],
                    y: -coordinates[1]
                };
            }
        }
        if (point) {
            mapData.push(extend(point, {
                name: properties.name || properties.NAME,
                /**
                 * In Highmaps, when data is loaded from GeoJSON, the GeoJSON
                 * item's properies are copied over here.
                 *
                 * @requires modules/map
                 * @name Highcharts.Point#properties
                 * @type {*}
                 */
                properties: properties
            }));
        }
    });
    // Create a credits text that includes map source, to be picked up in
    // Chart.addCredits
    if (series && geojson.copyrightShort) {
        series.chart.mapCredits = format(series.chart.options.credits.mapText, { geojson: geojson });
        series.chart.mapCreditsFull = format(series.chart.options.credits.mapTextFull, { geojson: geojson });
    }
    return mapData;
};
// Override addCredits to include map source by default
wrap(Chart.prototype, 'addCredits', function (proceed, credits) {
    credits = merge(true, this.options.credits, credits);
    // Disable credits link if map credits enabled. This to allow for in-text
    // anchors.
    if (this.mapCredits) {
        credits.href = null;
    }
    proceed.call(this, credits);
    // Add full map credits to hover
    if (this.credits && this.mapCreditsFull) {
        this.credits.attr({
            title: this.mapCreditsFull
        });
    }
});
