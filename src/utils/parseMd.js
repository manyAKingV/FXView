// 处理md文件
function parseMD(content) {
    if (!content) {
        return {
            name: '',
            describe: '',
            time: '',
            website: ''
        };
    }
    const cleanContent = content
        .replace(/<\/?p>/g, '')
        .replace(/<br\s*\/?>/g, '\n')
        .replace(/<\/?a[^>]*>/g, '');
    
    console.log(cleanContent);
    
    const patterns = {
        name: /名称[:：]\s*([^\n]+)/im,
        describe: /描述[:：]\s*((?:.|\n)+?)(?=\n\S+[:：]|$)/im,
        time: /成立时间[:：]\s*(\d{4}?)/im,
        website: /网站[:：]\s*([^\n]+)/i         
    };
    
    const result = {};
    for (const key in patterns) {
        const match = cleanContent.match(patterns[key]);
        if (key === 'tags') {
            result[key] = (match?.[1] || '').split(';').map(tag => tag.trim()).filter(Boolean);
        } else {
            result[key] = (match?.[1] || '').trim();
        }
    }

    return result;
}

module.exports = {
    parseMD
};