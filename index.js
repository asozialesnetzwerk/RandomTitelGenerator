function genWords(callback) {
    readFiles((rules, words) => {
        const ruleArr = [];
        for (const rule of rules.split("\n")) {
            ruleArr.push(rule.split("-"));
        }
        const newStr = [];
        let last = "qqqqq";
        words.split("\n").forEach(s => {
            const lower = s.toLowerCase();
            const lReplaced = replaceUmlauts(lower);
            if (s.length <= 28 //because of discords limitations
                && s.length > 2 //
                && (Math.abs(s.length - last.length) >= 3 || !lReplaced.startsWith(last))) {
                if (lower !== s) {
                    newStr.push(addArticle(lower, ruleArr));
                    if (!lReplaced.startsWith(last)
                        || lReplaced.length > last.length)
                        last = lReplaced;
                }
            }
        });
        if (typeof callback === "function") {
            callback(newStr);
        } else {
            console.log(newStr);
        }
    }, "rules.txt", "words.txt");
}

function replaceUmlauts(str) {
    return str.replace("ä", "a").replace("ö", "o").replace("ü", "u");
}

function readFiles(callback) {
    if (arguments.length <= 1) {
        console.error("Missing arguments.");
        return;
    }
    const promises = [];
    const texts = [];
    for (let i = 1; i < arguments.length; i++) {
        promises.push(fetch(arguments[i]).then(result => result.text()).then(str => texts[i - 1] = str));
    }
    Promise.all(promises).then(() => {
        callback.apply(callback, texts);
    }).catch(e => {
        console.error(e);
    });
}

function addArticle(strLower, rules) {
    //for (const rule of rules) {
    //    if (strLower.endsWith(rule[1])) {
    //        return rule[0] + firstCharToUppercase(strLower);
    //    }
    //}
    return firstCharToUppercase(strLower);
}

function firstCharToUppercase(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}
