---
modified: 2026-04-13T06:23:33+03:00
---
Honest breakdown of what's making it heavy:

**The biggest offender — `systeminformation`** The `currentLoad()` call to get CPU usage is genuinely expensive. It works by sampling CPU activity over a short interval, which means it's actively stressing the CPU to measure the CPU. Even at 3s intervals, each call spins up a measurement cycle. This is the fan culprit.

**Electron itself** Electron bundles a full Chromium browser + Node.js runtime. A "hello world" Electron app uses ~150MB RAM and a noticeable chunk of CPU just sitting idle. That's the baseline tax you pay for using web tech on the desktop.

**Running in dev mode** `npm run start` runs Vite's dev server AND Electron simultaneously. Vite watches every file for changes, runs HMR, keeps a full module graph in memory. This is significantly heavier than the built/packaged version. The `.exe` you built earlier is much lighter because Vite is gone and everything is pre-bundled.

**The file watcher** `fs.watch` on `data.json` fires on every write, including the writes the app itself makes. This can create a tight loop — app writes → watcher fires → app re-renders → app writes again. We added guards but it's still a source of unnecessary work.

**What to do:**

The quickest wins:

1. Remove `systeminformation` entirely and use only Node's built-in `os` module for RAM — no CPU measurement, no sampling overhead
2. Use the packaged `.exe` for daily use instead of `npm run start`
3. Debounce the file watcher so it doesn't fire more than once per second

Want me to strip out `systeminformation` and replace it with a lightweight alternative that just uses `os`?

C:\Users\user\Dev's Memory\devs-memory
cd devs-memory
npm run start
