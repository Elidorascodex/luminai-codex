/**
 * @file index.js or app.js
 * @description Bootstrap - Initialize and run LuminAI Codex system
 * Shows how to use the Cute Modular Architecture
 */

// Initialize OpenTelemetry tracing
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-otlp-grpc");
const {
  getNodeAutoInstrumentations,
} = require("@opentelemetry/auto-instrumentations-node");

const sdk = new NodeSDK({
  serviceName: "luminai-codex",
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTLP_ENDPOINT || "http://localhost:4317",
    headers: {},
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

require("dotenv").config();

const HarmonyNode = require("./lib/harmony");
const ResonanceEngine = require("./modules/resonance-engine");
const CodexHub = require("./modules/codex-hub");
const ArcadiaPortal = require("./modules/arcadia-portal");
// const LuminesceMonitor = require('./modules/luminescence-monitor');

/**
 * Initialize the LuminAI Codex System
 */
async function bootstrap() {
  console.log("\n🌟 LuminAI Codex - Cute Modular System\n");

  try {
    // 1. Create the Harmony Node (event bus)
    const harmony = new HarmonyNode({
      maxQueueSize: 10000,
      routeTimeout: 30000,
    });

    // 2. Create module instances
    const resonance = new ResonanceEngine();
    const codex = new CodexHub();
    const arcadia = new ArcadiaPortal();
    // const luminescence = new LuminesceMonitor();

    // 3. Set up dependencies
    // Example: CodexHub depends on Resonance working first
    codex.dependencies = [resonance];

    // 4. Register modules with Harmony
    harmony.registerModule(resonance);
    harmony.registerModule(codex);
    harmony.registerModule(arcadia);
    // harmony.registerModule(luminescence);    // 5. Initialize the system
    await harmony.initialize();

    // 6. Get system status
    const status = await harmony.getSystemStatus();
    console.log("\n📊 System Status:");
    console.log(`   Modules: ${status.totalModules}`);
    console.log(`   Messages Routed: ${status.metrics.messagesRouted}`);
    console.log(`   Harmony Status: ${status.harmonyStatus}\n`);

    // 7. Test the system
    await testSystem(harmony);

    // 8. Keep running (in production, this would be a server)
    // For now, demonstrate graceful shutdown
    setTimeout(async () => {
      console.log("\n🛑 Initiating graceful shutdown...\n");
      await harmony.shutdown();
      process.exit(0);
    }, 5000);
  } catch (error) {
    console.error("❌ Bootstrap failed:", error);
    process.exit(1);
  }
}

/**
 * Test the modular system
 */
async function testSystem(harmony) {
  console.log("🧪 Testing system...\n");

  const resonance = harmony.getModule("🧠 Resonance Engine");

  try {
    // Test 1: Simple thinking
    console.log("Test 1: Simple thought");
    const thought = await resonance.execute("think", {
      prompt: "What is the meaning of life?",
      provider: "openai",
    });
    const responseText =
      typeof thought === "string" ? thought : thought.response;
    console.log("  Response:", responseText.slice(0, 60) + "...\n");

    // Test 2: Brainstorming
    console.log("Test 2: Brainstorming");
    const ideas = await resonance.execute("brainstorm", {
      topic: "creative projects with AI",
      provider: "anthropic",
    });
    const ideasText = typeof ideas === "string" ? ideas : ideas.response;
    console.log("  Ideas:", ideasText.slice(0, 60) + "...\n");

    // Test 3: Summarization
    console.log("Test 3: Summarization");
    const summary = await resonance.execute("summarize", {
      text: "Modular architectures enable independent scaling, testing, and deployment of system components",
      provider: "xai",
    });
    const summaryText =
      typeof summary === "string" ? summary : summary.response;
    console.log("  Summary:", summaryText.slice(0, 60) + "...\n");

    // Test 4: Module status
    console.log("Test 4: Module Status");
    const status = await resonance.execute("getStatus", {});
  } catch (error) {
    console.error("❌ Test failed:", error.message);
  }
}

/**
 * Handle graceful shutdown
 */
process.on("SIGINT", async () => {
  console.log("\n\n🛑 Received shutdown signal");
  process.exit(0);
});

process.on("SIGTERM", async () => {
  console.log("\n\n🛑 Received termination signal");
  process.exit(0);
});

// Run bootstrap
if (require.main === module) {
  bootstrap();
}

module.exports = bootstrap;
