module.exports = function override(config, env) {
    config.resolve.fallback = {
      "http": require.resolve("stream-http"),
      "https": require.resolve("https-browserify"),
      "stream": require.resolve("stream-browserify"),
      "util": require.resolve("util/"),
      "url": require.resolve("url/"),
      "zlib": require.resolve("browserify-zlib"),
      "assert": require.resolve("assert/")
    };
    return config;
  };