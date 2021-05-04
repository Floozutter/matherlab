function fragload(fragments) {
    const promises = Array.from(fragments).map(([path, key]) => 
        fetch(path).then(r => r.text()).then(text => [key, text])
    );
    return Promise.all(promises).then((pairs) => new Map(pairs));
}
