function fragload(key_to_path) {
    const promises = Array.from(key_to_path).map(([key, path]) => 
        fetch(path).then(r => r.text()).then(text => [key, text])
    );
    return Promise.all(promises).then((pairs) => new Map(pairs));
}
