function change_filter_1(id) {
    let current_filter = document.querySelector('.activate_1');
    current_filter.classList.remove('activate_1');
    document.getElementById(id).classList.add('activate_1');
    item_filter(id);
}

function change_filter_2(id) {
    let current_filter = document.querySelector('.activate_2');
    current_filter.classList.remove('activate_2');
    document.getElementById(id).classList.add('activate_2');
    item_filter_1(id);
}

// Dark mode state
let isDarkMode = false;
if (localStorage.getItem('isDarkMode') !== null) {
    isDarkMode = localStorage.getItem('isDarkMode');
    if (isDarkMode === "true") {
        document.documentElement.style.setProperty("--title", "#D8D9DB");
        document.documentElement.style.setProperty("--white", "#093637");
        document.documentElement.style.setProperty("--top-section-white", "rgba(8, 31, 32, 1)");
        document.documentElement.style.setProperty("--black", "#ffffff");
        document.documentElement.style.setProperty("--company-name", "#ffffff");
        document.documentElement.style.setProperty("--paragraph-ash", "#CBE9E4");
        document.documentElement.style.setProperty("--description", "#CBE9E4");
        let greGradient = "linear-gradient(180deg, #081F20 0%, rgba(55, 60, 58, 1) 100%)";
        document.documentElement.style.setProperty("--gre-background", greGradient);
        let darkIcon = document.getElementById('dark-mode-icon');
        let lightIcon = document.getElementById('light-mode-icon');
        lightIcon.classList.remove('close');
        darkIcon.classList.add('close');
        isDarkMode = true;
    } else {
        isDarkMode = false;
    }
}

let isListView = true;

function viewToggle() {
    let gridViewIcon = document.getElementById('grid_view_icon');
    let listViewIcon = document.getElementById('list_view_icon');
    let itemListView = document.getElementById('item_list_view');
    let itemGridView = document.getElementById('item_grid_view');
    let comboListView = document.getElementById('combo_list_view');
    let comboGridView = document.getElementById('combo_grid_view');

    let item_list = document.querySelectorAll(".item_class")
    let combo_list = document.querySelectorAll(".combo_class")

    if (isListView === true) {
        gridViewIcon.classList.add('close');
        listViewIcon.classList.remove('close');
        isListView = false;
        itemListView.classList.add('close');
        itemGridView.classList.remove('close');
        comboListView.classList.add('close');
        comboGridView.classList.remove('close');
        item_list.forEach(function (item) {
            item.classList.add("display_block")
            item.classList.remove("display_flex")
        });

        combo_list.forEach(function (combo) {
            combo.classList.add("display_block")
            combo.classList.remove("display_flex")
        });
    } else {
        gridViewIcon.classList.remove('close');
        listViewIcon.classList.add('close');
        isListView = true;
        itemListView.classList.remove('close');
        itemGridView.classList.add('close');
        comboListView.classList.remove('close');
        comboGridView.classList.add('close');
        item_list.forEach(function (item) {
            item.classList.add("display_flex")
            item.classList.remove("display_block")
        });

        combo_list.forEach(function (combo) {
            combo.classList.add("display_flex")
            combo.classList.remove("display_block")
        });
    }
}

// ThemeChange

function ThemeToggle() {
    let darkIcon = document.getElementById('dark-mode-icon');
    let lightIcon = document.getElementById('light-mode-icon');
    if (isDarkMode === false) {
        lightIcon.classList.remove('close');
        darkIcon.classList.add('close');
        let greGradient = "linear-gradient(180deg, #081F20 0%, rgba(55, 60, 58, 1) 100%)";
        document.documentElement.style.setProperty("--title", "#D8D9DB");
        document.documentElement.style.setProperty("--white", "#093637");
        document.documentElement.style.setProperty("--top-section-white", "rgba(8, 31, 32, 1)");
        document.documentElement.style.setProperty("--black", "#ffffff");
        document.documentElement.style.setProperty("--border-bottom-light", "#708e88");
        document.documentElement.style.setProperty("--company-name", "#ffffff");
        document.documentElement.style.setProperty("--description", "#CBE9E4");
        document.documentElement.style.setProperty("--gre-background", greGradient);
        isDarkMode = true;
        localStorage.setItem('isDarkMode', isDarkMode)
    } else {
        lightIcon.classList.add('close');
        darkIcon.classList.remove('close');
        document.documentElement.style.setProperty("--title", "#295647");
        document.documentElement.style.setProperty("--white", "#ffffff");
        document.documentElement.style.setProperty("--black", "#242424");
        document.documentElement.style.setProperty("--border-bottom-light", "#c7dbd7");
        document.documentElement.style.setProperty("--top-section-white", "#ffffff");
        document.documentElement.style.setProperty("--description", "#295647");
        document.documentElement.style.setProperty("--company-name", "#49454F");
        document.documentElement.style.setProperty("--gre-background", "linear-gradient(180deg, #E7FFFB 0%, #EBEBEB 100%)");
        isDarkMode = false;
        localStorage.setItem('isDarkMode', isDarkMode)

    }


}

function insert_item_video_link(link, id) {
    $("#" + id).attr("src", link);
    console.log(link)
}

// item list view filter
const item_container_list_view = document.getElementById("item_container");
const items_list_view = item_container_list_view.querySelectorAll('.item_class');
// item grid view
const item_container_grid_view = document.getElementById("item_container_1");
const items_grid_view = item_container_grid_view.querySelectorAll('.item_class');

function item_filter(id) {
    let filterQuery_list = id.split('_');
    let filterQuery = filterQuery_list[1].toLowerCase();
    items_list_view.forEach((item) => {
        let itemCategory = item.querySelector('.items_category').value.toLowerCase();
        if (itemCategory.includes(filterQuery)) {
            item.classList.remove('stash');
            item.classList.add('showStash');
        } else if (filterQuery === "item") {
            item.classList.remove('stash');
            item.classList.add('showStash');
        } else {
            item.classList.remove('showStash');
            item.classList.add('stash');
        }
    });
    items_grid_view.forEach((item) => {
        let itemCategory = item.querySelector('.items_category').value.toLowerCase();
        if (itemCategory.includes(filterQuery)) {
            item.classList.remove('stash');
            item.classList.add('showStash');
        } else if (filterQuery === "item") {
            item.classList.remove('stash');
            item.classList.add('showStash');
        } else {
            item.classList.remove('showStash');
            item.classList.add('stash');
        }
    });
}

// item list view filter end


// combo list view
const combo_container_list_view = document.getElementById("combo_container");
const combo_list_view = combo_container_list_view.querySelectorAll('.combo_class');
// combo grid view
const combo_container_grid_view = document.getElementById("combo_container_1");
const combo_grid_view = combo_container_grid_view.querySelectorAll('.combo_class');

function item_filter_1(id) {
    let filterQuery_list = id.split('_');
    let filterQuery = filterQuery_list[1].toLowerCase();
    combo_list_view.forEach((combo) => {
        let comboCategory = combo.querySelector('.group_category').value.toLowerCase();
        if (comboCategory.includes(filterQuery)) {
            combo.classList.remove('stash');
            combo.classList.add('showStash');
        } else if (filterQuery === "combo") {
            combo.classList.remove('stash');
            combo.classList.add('showStash');
        } else {
            combo.classList.remove('showStash');
            combo.classList.add('stash');
        }
    });
    combo_grid_view.forEach((combo) => {
        let comboCategory = combo.querySelector('.group_category').value.toLowerCase();
        if (comboCategory.includes(filterQuery)) {
            combo.classList.remove('stash');
            combo.classList.add('showStash');
        } else if (filterQuery === "combo") {
            combo.classList.remove('stash');
            combo.classList.add('showStash');
        } else {
            combo.classList.remove('showStash');
            combo.classList.add('stash');
        }
    });
}
