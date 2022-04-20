// vue.config.js

//const REAL_APP_SERVER = "https://185.23.163.212:5001";
const REAL_APP_SERVER = process.env.VUE_APP_REAL_SERVER_URL

module.exports = {
    devServer: {
      proxy: {
        "/app": {
          target: REAL_APP_SERVER,
          changeOrigin: true,
          secure: false
        },
        "/task": {
            target: REAL_APP_SERVER,
            changeOrigin: true,
            secure: false
          },
        "/dev": {
            target: REAL_APP_SERVER,
            changeOrigin: true,
            secure: false
        },
        "/editor": {
            target: REAL_APP_SERVER,
            changeOrigin: true,
            secure: false
        },
        "/debug": {
            target: REAL_APP_SERVER,
            changeOrigin: true,
            secure: false
        },
        "/resource": {
            target: REAL_APP_SERVER,
            changeOrigin: true,
            secure: false
        },
        "/Login": {
          target: REAL_APP_SERVER,
          changeOrigin: true,
          secure: false
      },


      }
    }
  };