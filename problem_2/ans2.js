const input = [{
    "manager_name": "nssi",
    "login_name": "nishanthi"
}, {
    "manager_name": "mbarcelona",
    "login_name ": "nssi"
}, {
    "manager_name": "nishanthi",
    "login_name": "markcorderoi"
}, {
    "manager_name": "mbarcelona",
    "login_name ": "richard"
}, {
    "manager_name": "letecia",
    "login_name ": "rudy"
}]

const map = {};

const cleaned = input.map(item => ({
    manager_name: item.manager_name.trim(),
    login_name: (item.login_name || item["login_name "]).trim()
}))


cleaned.forEach(({ manager_name, login_name }) => {
    if (!map[manager_name]) {
        map[manager_name] = { name: manager_name, subordinate: [] };
    }
    if (!map[login_name]) {
        map[login_name] = { name: login_name };
    }
});

cleaned.forEach(({ manager_name, login_name }) => {
    if (!map[manager_name].subordinate) {
        map[manager_name].subordinate = [];
    }

    map[manager_name].subordinate.push(map[login_name]);
});

const allSubordinates = new Set(cleaned.map(({ login_name }) => login_name));
const topManagers = Object.values(map).filter(
    person => !allSubordinates.has(person.name)
);

function cleanSubordinate(node) {
    if (node.subordinate) {
        node.subordinate = node.subordinate.map(cleanSubordinate);
        if (node.subordinate.length === 0) {
            delete node.subordinate;
        }
    }
    return { ...node };
}

const output = topManagers.map(cleanSubordinate);

console.log(JSON.stringify(output, null, 2));
