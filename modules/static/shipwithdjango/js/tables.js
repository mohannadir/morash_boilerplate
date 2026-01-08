/**
 * @file tables.js
 * @brief JavaScript for dynamic tables.
 * @details This file contains JavaScript for initializing and managing dynamic tables.
 * A dynamic table is a table that is populated with data from the server.
 */

import EventHandler from './events.js';

/**
 * Initializes all tables with the class 'dynamic' by fetching the table data from the server.
 */
document.addEventListener('DOMContentLoaded', function() {
    initDynamicTables();
    initClickableTableRows();
});

/**
 * Initializes all tables with the class 'dynamic'.
*/
function initDynamicTables() {
    const dynamicTables = document.querySelectorAll('table.dynamic');
    for (const table of dynamicTables) {
        initDynamicTable(table);
    }
}

/**
 * Initializes a table by fetching the table data from the server.
 * The table data is fetched from the URL specified in the data-url attribute of the table.
 * The table is then populated with the data returned from the server.
 */
function initDynamicTable(table) {
    table.classList.add('w-full');

    populateTable(table, generateTableSkeletonHTML());
    const wrapper = document.createElement('div');
    wrapper.classList.add('table-wrapper', 'w-full', 'overflow-x-auto');
    const actionWrapper = document.createElement('div');
    const bottomWrapper = document.createElement('div');
    actionWrapper.classList.add('actions', 'flex', 'justify-end', 'space-x-2', 'mb-2');
    bottomWrapper.classList.add('table-bottom', 'flex', 'justify-between', 'items-center', 'mt-4');

    const tableParent = table.parentNode;

    let url = table.getAttribute('data-url');
    const sortSelect = tableParent.querySelector('select.sort');
    if (sortSelect) {
        url += `?sort_field=${sortSelect.value}`;
    }
    
    fetch(url, getFetchInit('GET'))
        .then(response => response.json())
        .then(data => {
            populateTable(table, data.html);

            if(data.total > 0) {
                addSearchField(table);
                addSortOptions(table, data.sort_options, data.sort_default);
                addPerPageOptions(table, data.per_page);
                addPaginationControls(table, data.page, data.num_pages, data.per_page, data.total);
            } else {
                table.querySelector('thead').remove();
            }

            initClickableRows(table);
        });
        
    // Adds the actionWrapper and the table to the wrapper. The wrapper is then added to the tableParent.
    // And then put the new div in the same place as the table.
    wrapper.appendChild(actionWrapper);
    wrapper.appendChild(table);
    wrapper.appendChild(bottomWrapper);
    tableParent.appendChild(wrapper);
}

/**
 * Returns a fetch init object with the given method and body.
 * @param {string} method The HTTP method to use.
 * @param {Object} body The body of the request.
 * @returns {Object} A fetch init object.
 */
function getFetchInit(method, body) {
    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const headers = new Headers({
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf
    });
    const init = {
        method: method,
        headers: headers,
        credentials: 'same-origin',
        cache: 'no-cache'
    };

    if (body) {
        init.body = JSON.stringify(body);
    }

    return init;
}

/**
 * Populates the table with the given HTML.
 */
function populateTable(table, html) {
    table.innerHTML = html;
    feather.replace();
}

/**
 * Adds a select element above the table with options for sorting the table.
 * @param {HTMLTableElement} table The table to add sorting options to.
 * @param {Array} sortOptions An array of objects with name and field properties.
 */
function addSortOptions(table, sortOptions, sortDefault) {
    if(sortOptions.length == 0) {
        return;
    }

    const wrapper = table.parentNode.querySelector('div.actions');

    const selectFieldHtml = `
        <div class="relative">
            <select class="sort w-full outline-0 rounded-md border-slate-300 p-2 text-gray-600 shadow-xs pr-12">
            </select>
        </div>
    `;

    const sortSelect = document.createElement('div');
    sortSelect.innerHTML = selectFieldHtml;
    let sortSelectField = sortSelect.querySelector('select.sort');

    for (const option of sortOptions) {
        const optionElement = document.createElement('option');
        optionElement.value = option.field;
        optionElement.textContent = option.name;
        if (sortDefault && sortDefault == option.field) {
            optionElement.selected = true;
        }
        sortSelectField.appendChild(optionElement);
    }

    sortSelectField.addEventListener('change', function() {
        searchAndSortTable(table);
    });

    wrapper.appendChild(sortSelect);
}

/**
 * Adds a search input field above the table.
 */
function addSearchField(table) {
    const wrapper = table.parentNode.querySelector('div.actions');

    const searchFieldHtml = `
        <div class="relative"> 
            <input type="text" class="w-full outline-0 rounded-md border-slate-300 p-2 text-default shadow-xs search" placeholder="Search..." /> 
            <div class="pointer-events-none w-8 h-8 absolute top-1/2 transform -translate-y-1/2 right-3 flex items-center justify-center"> 
                <i class="text-slate-500" data-feather="search" width="18px" height="18px"></i> 
            </div> 
        </div>
    `;

    const searchField = document.createElement('div');
    searchField.innerHTML = searchFieldHtml;
    const searchFieldInput = searchField.querySelector('input.search');

    let debounceTimeout; // Used to debounce the input event.
    searchFieldInput.addEventListener('input', function() {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(function() {
            searchAndSortTable(table);
        }, 300);
    });

    wrapper.appendChild(searchField);
}

/**
 * Adds pagination controls below the table.
 */
function addPaginationControls(table, currentPage, numPages, itemsPerPage, totalItems) {
    const wrapper = table.parentNode.querySelector('div.table-bottom');
    const paginationWrapper = document.createElement('div');
    paginationWrapper.classList.add('pagination', 'flex', 'justify-center', 'space-x-2', 'mt-4');

    const createPageButton = (page, text = null) => {
        const pageButton = document.createElement('button');
        pageButton.type = 'button';
        pageButton.textContent = text || page;
        pageButton.classList.add('page-btn', 'px-4', 'py-2', 'rounded-2xl', 'bg-primary-light', 'text-primary');
        if (page == currentPage) {
            pageButton.classList.remove('bg-primary-light', 'text-primary');
            pageButton.classList.add('font-bold', 'bg-primary', 'text-white');
        }
        pageButton.addEventListener('click', (event) => {
            event.preventDefault();
            searchAndSortTable(table, page);
        });
        return pageButton;
    };

    const addEllipsis = () => {
        const ellipsis = document.createElement('span');
        ellipsis.textContent = '...';
        ellipsis.classList.add('px-4', 'py-2');
        paginationWrapper.appendChild(ellipsis);
    };

    if (currentPage > 1) {
        paginationWrapper.appendChild(createPageButton(currentPage - 1, 'Previous'));
    }

    paginationWrapper.appendChild(createPageButton(1));

    if (currentPage > 3) {
        addEllipsis();
    }

    for (let page = Math.max(2, currentPage - 2); page <= Math.min(numPages - 1, currentPage + 2); page++) {
        paginationWrapper.appendChild(createPageButton(page));
    }

    if (currentPage < numPages - 2) {
        addEllipsis();
    }

    if (numPages > 1) {
        paginationWrapper.appendChild(createPageButton(numPages));
    }

    if (currentPage < numPages) {
        paginationWrapper.appendChild(createPageButton(currentPage + 1, 'Next'));
    }

    const existingPagination = wrapper.querySelector('.pagination');
    if (existingPagination) {
        existingPagination.remove();
    }

    const showingItemsWrapper = document.createElement('div');
    showingItemsWrapper.textContent = `Showing ${Math.min((currentPage - 1) * itemsPerPage + 1, totalItems)} to ${Math.min(currentPage * itemsPerPage, totalItems)} of ${totalItems} items`;
    showingItemsWrapper.classList.add('showing-items', 'text-sm', 'text-slate-500');

    const existingShowingItems = wrapper.querySelector('.showing-items');
    if (existingShowingItems) {
        existingShowingItems.remove();
    }

    wrapper.appendChild(showingItemsWrapper);
    wrapper.appendChild(paginationWrapper);
}

/**
 * Adds a select element above the table with options for the number of items to show per page.
 */
function addPerPageOptions(table, perPageDefault) {
    const wrapper = table.parentNode.querySelector('div.actions');

    const perPageOptions = [10, 25, 50, 100];
    const selectFieldHtml = `
        <div class="relative">
            <select class="per-page w-full outline-0 rounded-md border-slate-300 p-2 text-gray-600 shadow-xs pr-12">
            </select>
        </div>
    `;

    const perPageSelect = document.createElement('div');
    perPageSelect.innerHTML = selectFieldHtml;
    let perPageSelectField = perPageSelect.querySelector('select.per-page');

    for (const option of perPageOptions) {
        const optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.textContent = `Show ${option}`;
        if (perPageDefault && perPageDefault == option) {
            optionElement.selected = true;
        }
        perPageSelectField.appendChild(optionElement);
    }

    perPageSelectField.addEventListener('change', function() {
        searchAndSortTable(table);
    });

    wrapper.appendChild(perPageSelect);
}

/**
 * Fetches the table data from the server and populates the table with the returned data.
 */
function searchAndSortTable(table, page = 1) {
    populateTable(table, generateTableSkeletonHTML());
    let url = table.getAttribute('data-url');
    let params = new URLSearchParams();
    const sortSelect = table.parentNode.querySelector('select.sort');
    const searchField = table.parentNode.querySelector('input.search');
    const perPageSelect = table.parentNode.querySelector('select.per-page');

    if(!sortSelect && !searchField) {
        return;
    }

    if(sortSelect && sortSelect.value != 'none') {
        params.set('sort_field', sortSelect.value);
    }

    if(searchField && searchField.value && searchField.value != '') {
        params.set('search', searchField.value);
    }

    if (perPageSelect) {
        params.set('per_page', perPageSelect.value);
    }

    params.set('page', page);

    const full_url = url + '?' + params.toString();
    fetch(full_url, getFetchInit('GET'))
        .then(response => response.json())
        .then(data => {
            populateTable(table, data.html);
            addPaginationControls(table, data.page, data.num_pages, data.per_page, data.total);
            initClickableRows(table);
        });

}

/**
 * Generates HTML for a skeleton table.
 * @returns {string} HTML for a skeleton table.
 */
function generateTableSkeletonHTML() {
    return `
    <div class="my-3 animate-pulse text-card border-separate space-y-4 text-sm border-spacing-x-0 border-spacing-y-4 w-full">
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
        <div class="bg-slate-100 rounded-xl h-12">
            <div class="rounded-l-xl"></div>
            <div></div>
            <div class="rounded-r-xl"></div>
        </div>
    </div>
    `;
}

/**
 * Initializes clickable rows in tables.
 */
function initClickableTableRows() {
    const tables = document.querySelectorAll('table.clickable-rows');
    for (const table of tables) {
        initClickableRows(table);
    }
}

/**
 * Initializes clickable rows in a table.
 */
function initClickableRows(table) {
    const rows = table.querySelectorAll('tr[data-href]');
    for (const row of rows) {
        let href = row.getAttribute('data-href');
        if(!href || href == '') {
            continue;
        }

        const clickableTds = row.querySelectorAll('td:not(.no-click)');
        if(!clickableTds) {
            continue;
        }

        for (const td of clickableTds) {
            const eventHandler = new EventHandler(td);
            eventHandler.removeEvent('click.clickable-rows');
            eventHandler.addEvent('click.clickable-rows', function() {
                window.location.href = href;
            });
        }
    }
}