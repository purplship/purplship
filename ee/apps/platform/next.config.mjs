import { withSentryConfig } from "@sentry/nextjs";
import path from "path";

/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    transpilePackages: [
        "@karrio/core",
        "@karrio/hooks",
        "@karrio/ui",
        "@karrio/lib",
        "@karrio/types",
        "@karrio/insiders",
        "@karrio/console"
    ],
    sentry: {
        disableServerWebpackPlugin: true,
        disableClientWebpackPlugin: true,
    },
    sassOptions: {
        includePaths: [path.join("src", "app", "styles")],
    },
    webpack: (config) => {
        config.resolve.fallback = { fs: false, net: false, tls: false };
        config.externals.push("pino-pretty", "encoding");
        return config;
    }
};

const sentryWebpackPluginOptions = {
    // Additional config options for the Sentry Webpack plugin. Keep in mind that
    // the following options are set automatically, and overriding them is not
    // recommended:
    //   release, url, org, project, authToken, configFile, stripPrefix,
    //   urlPrefix, include, ignore

    silent: true, // Suppresses all logs
    // For all available options, see:
    // https://github.com/getsentry/sentry-webpack-plugin#options.
};

export default withSentryConfig(nextConfig, sentryWebpackPluginOptions);
