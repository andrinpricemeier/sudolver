const asciidoctor = require("@asciidoctor/core")();
const kroki = require("asciidoctor-kroki");

const input = "plantuml::hello.puml[svg,role=sequence]";

kroki.register(asciidoctor.Extensions); // <1>
console.log(asciidoctor.convert(input, { safe: "safe" }));

const registry = asciidoctor.Extensions.create();
kroki.register(registry); // <2>
console.log(
  asciidoctor.convert(input, { safe: "safe", extension_registry: registry })
);
