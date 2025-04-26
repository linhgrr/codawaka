module.exports = {
  // Enable runtime compilation for templates
  runtimeCompiler: true,
  
  // Configure webpack to define environment variables
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      Object.assign(args[0]['process.env'], {
        VUE_APP_API_URL: JSON.stringify(process.env.VUE_APP_API_URL || 'http://localhost:8000')
      })
      return args
    })
  }
}