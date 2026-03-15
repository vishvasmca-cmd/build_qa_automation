# 🧪 eCommerce Autonomous QA - Testing Guide

## Quick Start (5 Minutes)

### 1️⃣ Load Extension in Chrome

1. Open Chrome browser
2. Navigate to: `chrome://extensions/`
3. Enable **Developer mode** (toggle in top-right corner)
4. Click **"Load unpacked"**
5. Select folder: `C:\Users\vishv\.gemini\antigravity\playground\inner-event\chrome-extension`
6. ✅ Extension should appear with blue/cyan robot icon

### 2️⃣ Configure Gemini API Key

1. Click the extension icon in Chrome toolbar (or from Extensions menu)
2. Enter your **Gemini API Key**
   - Don't have one? Get it FREE at: https://aistudio.google.com/app/apikey
   - Takes 30 seconds to create
3. Select model: **Gemini 2.0 Flash (Fastest)** (recommended)
4. Click **"Save Configuration"**
5. Wait for ✅ "Configuration saved successfully"

### 3️⃣ Run Your First Test

#### **Test #1: Valid Login (Easiest)**

1. Navigate to: `https://www.saucedemo.com`
2. Click extension icon
3. Click: **"✅ Valid Login Test"** button
4. Click: **"🚀 Start Autonomous Test"**
5. **Watch the sidebar appear!** 🎉

**What you should see:**
- Blue sidebar slides in from right
- "SCENARIO 1: Valid Login Test" header
- ACT/VALIDATE/STATUS entries
- Green "PASS" indicators
- Live cart count updates

---

## 🧪 Test Suite

### Test #2: Unauthorized Access

1. Stay on `https://www.saucedemo.com`
2. Click extension icon
3. Click: **"🚫 Unauthorized Access Test"**
4. Click: **"🚀 Start Autonomous Test"**

**Expected:** Should show red "FAIL" when trying `locked_out_user`

---

### Test #3: Cart & Checkout

1. Login first (use Test #1)
2. Click extension icon
3. Click: **"💰 Single Product Checkout"**
4. Click: **"🚀 Start Autonomous Test"**

**Expected:** 
- Adds product
- Shows cart count (1)
- Navigates to checkout
- Validates price

---

### Test #4: Custom Goal

1. Navigate to any e-commerce site
2. Click extension icon
3. Type your own goal, e.g.:
   ```
   Login as standard_user, add 3 products, verify cart total
   ```
4. Click: **"🚀 Start Autonomous Test"**

---

## 🐛 Troubleshooting

### Extension Not Loading

**Symptom:** Error when loading unpacked extension

**Fix:**
1. Check Chrome console: `Ctrl+Shift+I` → Console tab
2. Look for error messages
3. Common issues:
   - **Module errors**: Make sure all `.js` files are saved
   - **Manifest errors**: Verify `manifest.json` is valid JSON

---

### "API Key Invalid"

**Symptom:** Error message in popup

**Fix:**
1. Verify your API key at: https://aistudio.google.com/app/apikey
2. Make sure you copied the FULL key (starts with `AIza...`)
3. Check for extra spaces when pasting

---

### Sidebar Not Appearing

**Symptom:** Test starts but no sidebar shows

**Fix:**
1. Open browser console: `Ctrl+Shift+I` → Console
2. Look for JavaScript errors
3. Refresh the page and try again
4. Check if content script is injected:
   ```javascript
   // In console, type:
   window.agAddEntry
   // Should return: function
   ```

---

### Elements Not Found

**Symptom:** "Element not found" errors in sidebar

**Fix:**
1. The AI might not recognize element descriptions
2. Try more specific goal descriptions:
   - ❌ Bad: "Click the button"
   - ✅ Good: "Click the 'Add to Cart' button"
3. Check if the site structure is compatible

---

## 📊 Success Criteria

Your extension is working correctly if you see:

✅ **Sidebar appears** on test start
✅ **Scenarios are demarcated** with orange headers
✅ **ACT/VALIDATE/STATUS phases** are clearly labeled
✅ **Plain English descriptions** (no technical jargon)
✅ **Pass/Fail indicators** are green/red
✅ **Cart count updates** in real-time
✅ **Mission Report** appears at the end

---

## 🎥 What Happens During a Test

1. **AI Receives Goal** → Gemini generates test plan
2. **Scenarios Created** → Multiple test cases with steps
3. **DOM Automation** → Browser-native click/fill actions
4. **Smart Element Finding** → 9 fallback locator strategies
5. **WebMCP Validation** → Cart/price/checkout verification
6. **Real-time Logging** → Sidebar updates on each step
7. **Final Report** → Summary with pass/fail counts

---

## 🔍 Debugging Tips

### View Extension Logs

**Background Script:**
1. Go to: `chrome://extensions/`
2. Find "eCommerce Autonomous QA"
3. Click "Inspect views: service worker"
4. Check Console for AI reasoning logs

**Content Script:**
1. Open page with test running
2. Press `Ctrl+Shift+I` (DevTools)
3. Console tab shows sidebar logs

---

### Common Console Messages

**Good Signs:**
```
[QA-AGENT] Content script loaded
[QA-REASONING] Generating test plan: ...
[ELEMENT-FINDER] Found via strategy: byId
[DOM-ACTIONS] Clicking element: ...
[QA-SIDEBAR] Sidebar injected successfully
```

**Warning Signs:**
```
[ELEMENT-FINDER] No element found for: "..."
[Gemini] Error: API key invalid
[DOM-ACTIONS] Element is null or undefined
```

---

## 🎯 Next Steps After Testing

Once basic tests work:

1. **Try Different E-commerce Sites:**
   - Amazon
   - eBay  
   - Shopify stores
   - Your own company's site

2. **Create Custom Test Goals:**
   - Multi-step checkout flows
   - Coupon code validation
   - Guest checkout
   - Wishlist functionality

3. **Enhance the Extension:**
   - Add screenshot capture on failures
   - Export test reports as PDF
   - Create test history dashboard
   - Add Slack/Email notifications

---

## 📞 Getting Help

If you encounter issues:

1. **Check this guide first** (Troubleshooting section)
2. **Review browser console** for error messages
3. **Verify API key** is valid and has quota remaining
4. **Test on SauceDemo first** (known working site)
5. **Check Gemini API status:** https://status.cloud.google.com/

---

## 🎉 Success!

If you see tests running with the sidebar showing Pass/Fail results, **congratulations!** You now have a fully functional, browser-native AI QA agent! 🚀

Time to test your production e-commerce site! 💪
