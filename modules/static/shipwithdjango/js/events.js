/**
 * @file events.js
 * @brief JavaScript for managing events.
 * @details This file contains JavaScript for managing events.
 */

/**
 * @class EventHandler
 * @classdesc This class allows for namespacing of events and adding/removal of specific events and callbacks.
 */
export default class EventHandler {
    constructor(element) {
        this.element = element;
        this.functionMap = {};
    }

    addEvent(event, func) {
        const eventWithoutNamespace = event.split('.')[0];
        this.functionMap[eventWithoutNamespace] = func;
        this.element.addEventListener(eventWithoutNamespace, func);
    }

    removeEvent(event) {
        const eventWithoutNamespace = event.split('.')[0];
        this.element.removeEventListener(eventWithoutNamespace, this.functionMap[eventWithoutNamespace]);
    }
}