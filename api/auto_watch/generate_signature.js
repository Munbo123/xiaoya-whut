// 导入必要的库
const crypto = require('crypto');

/**
 * 签名帮助类
 */
class SignatureHelper {
    /**
     * 创建签名
     * @param {Object} n - 包含message、timestamp和nonce的对象
     * @returns {Object} 包含生成的签名和原始参数的对象
     */
    static createSignature(n) {
        // 创建包含编码后message的数组
        const r = [encodeURIComponent(n.message)];
        
        // 确定timestamp
        let i;
        if (n.timestamp) {
            i = n.timestamp;
        } else {
            i = new Date().getTime().toString();
        }
        
        // 确定nonce
        let o;
        if (n.nonce) {
            o = n.nonce;
        } else {
            o = SignatureHelper.createNonceStr();
        }
        
        // 将这些值添加到数组中
        r.push(i);
        r.push(o);
        r.push("--xy-create-signature--");
        
        // 数组排序，连接成字符串，然后SHA1加密
        const a = crypto.createHash('sha1').update(r.sort().join("")).digest('hex');
        
        // 返回包含原始message和生成的签名等信息的字典
        return {
            message: n.message,
            signature: a,
            timestamp: i,
            nonce: o
        };
    }

    /**
     * 创建随机nonce字符串
     * @param {number} n - 字符串长度，默认16
     * @returns {string} 随机字符串
     */
    static createNonceStr(n = 16) {
        const NONCE_STR_MAX = 32;
        n = Math.min(n, NONCE_STR_MAX);
        const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        let result = "";
        for (let i = 0; i < n; i++) {
            result += chars[Math.floor(Math.random() * chars.length)];
        }
        return result;
    }

    /**
     * 验证签名
     * @param {Object} n - 包含message、signature、timestamp和nonce的对象
     * @returns {boolean} 签名是否正确
     */
    static checkSignature(n) {
        const { signature: r } = SignatureHelper.createSignature(n);
        return r === n.signature;
    }
}

// 测试函数 - 尝试复现特定的签名
function testReproduceSpecificSignature() {
    // 使用给定的输入数据
    const testMessage = '{"video_id":"107dcd2a2a2271f088b06733a68f0102","played":30.16,"media_type":1,"duration":403.64,"watched_duration":30.154322}';
    const testNonce = "e239edfb-d015-44bd-9028-37ee61042380";
    const testTimestamp = "1746772507287";
    const expectedSignature = "610f8bddfd4391e7d18dc628f055234747b10f20";
    
    console.log("原始输入数据:");
    console.log(`message: ${testMessage}`);
    console.log(`nonce: ${testNonce}`);
    console.log(`timestamp: ${testTimestamp}`);
    
    // JavaScript的URL编码
    const encodedMessage = encodeURIComponent(testMessage);
    console.log(`JavaScript URL编码后的message: ${encodedMessage}`);
    
    // 创建排序前的数组
    const r = [encodedMessage, testTimestamp, testNonce, "--xy-create-signature--"];
    console.log(`排序前的数组: ${JSON.stringify(r)}`);
    
    // 排序数组
    const sortedR = [...r].sort();
    console.log(`排序后的数组: ${JSON.stringify(sortedR)}`);
    
    // 连接字符串
    const joinedStr = sortedR.join("");
    console.log(`连接后的字符串: ${joinedStr}`);
    
    // 计算SHA1
    const signature = crypto.createHash('sha1').update(joinedStr).digest('hex');
    console.log(`计算得到的signature: ${signature}`);
    console.log(`预期的signature: ${expectedSignature}`);
    console.log(`匹配结果: ${signature === expectedSignature}`);
    
    // 使用函数计算
    const testSignatureResult = SignatureHelper.createSignature({
        message: testMessage,
        nonce: testNonce,
        timestamp: testTimestamp
    });
    
    console.log("\n使用createSignature函数计算:");
    console.log(`生成的signature: ${testSignatureResult.signature}`);
    console.log(`预期的signature: ${expectedSignature}`);
    console.log(`匹配结果: ${testSignatureResult.signature === expectedSignature}`);
}

// 运行测试
testReproduceSpecificSignature();
