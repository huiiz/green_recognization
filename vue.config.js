const path = require("path");

function resolve(dir) {
    return path.join(__dirname, dir);
}

module.exports = {
    publicPath: "./",
    lintOnSave: false,
    devServer: {
        // can be overwritten by process.env.HOST
        host: "0.0.0.0",
        port: 8080,
    },
    chainWebpack: (config) => {
        config.resolve.alias
            .set("@", resolve("src"))
            .set("src", resolve("src"))
            .set("common", resolve("src/common"))
            .set("components", resolve("src/components"));
    },
    pluginOptions: {
        electronBuilder: {
            builderOptions: {
                win: {
                    icon: "./public/app.ico",
                },
                asar: false,
                extraResources: [
                    './pydist/**'
                ],
                artifactName: '${productName}_Setup_${version}_${platform}.${ext}',
                productName: '绿化先锋——基于深度学习的绿化信息提取与绿化率提升系统',
                nsis: {
                    // include: 'installer.nsh',
                    oneClick: false,
                    allowToChangeInstallationDirectory: true,
                    perMachine: true,
                    // 允许请求提升。 如果为false，则用户必须使用提升的权限重新启动安装程序。
                    allowElevation: true,
                    shortcutName: '${productName}',
                },
            },
        },
    },
};
