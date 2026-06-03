# Reddit Findings — Round 3

> Focus: Security incident timelines, community reactions, supply chain forensics

## Key Threads Not Covered in Rounds 1-2

### 1. r/selfhosted — Complete 2026 Security Incident Timeline
- **Thread:** "If you're self-hosting OpenClaw, here's every documented security incident in 2026"
- **Author:** u/LostPrune2143
- **Link:** https://www.reddit.com/r/selfhosted/comments/1r9yrw1/
- **Stats:** 35+ comments

**Incident summary from thread:**
- 6 CVEs documented in 2026
- 824+ malicious skills in ClawHub (up from 341 when first discovered)
- 42,000+ exposed OpenClaw instances found
- Links to detailed blog post at blog.barrack.ai

**Notable community reactions:**
- u/Skyobliwind: "Malicious skills actually make it quite unusable. Even if I'm more experienced and know what I do, that would require me to check every single skill for malicious behavior. Something like that really would require a moderated and audited marketplace for skills."
- u/WhoKnewTech: "The mother of all botnets." / "the guy who created it was hired by OpenAI after"
- u/LostPrune2143 (OP): "the adoption curve is way ahead of the security awareness curve. People are giving OpenClaw full disk access, terminal permissions, and OAuth tokens without realizing what that actually means."
- u/obtuseperuse: "how on earth anyone can look at the 'fcks things up machine' and go 'what if I gave it the ability to execute code autonomously'"
- u/Mx772: "I've also seen lots of non-tech people setting it up... they are missing the 'building blocks' concepts like security first, and are just like kids in a candy shop picking up everything"

**Takeaway:** Security is not abstract — self-hosting community is documenting real incidents. The gap between adoption speed and security awareness is explicitly recognized as the core problem.

### 2. r/openclaw — capability-evolver Data Exfiltration (14K Downloads)
- **Thread:** "PSA: capability-evolver skill (14K downloads) exfiltrates your data to ByteDance's Feishu"
- **Author:** u/SUTRA8
- **Link:** https://www.reddit.com/r/openclaw/comments/1qz8bqk/
- **Key detail:** "This is the second major supply chain incident this week after the ClawHavoc campaign (341 malicious packages found). ClawHub's only publishing..."
- **Scale:** 14,000 downloads of a single malicious skill exfiltrating to ByteDance/Feishu
- **Significance:** First documented state-adjacent actor targeting agent skills ecosystem

### 3. r/better_claw — ClawHavoc Campaign Timeline
- **URL:** https://www.reddit.com/r/better_claw/
- **Community-maintained timeline:**
  - Feb 1, 2026: Koi Security names "ClawHavoc" campaign, 341 malicious skills identified
  - Feb 4, 2026: DepthFirst and Snyk find incomplete fix
  - Ongoing documentation of remediation efforts
- **Significance:** Dedicated subreddit tracking the ongoing security crisis

### 4. r/AI_Agents — 50+ OpenClaw Alternatives
- **Thread:** "50+ OpenClaw Alternatives for Business"
- **Link:** https://www.reddit.com/r/AI_Agents/comments/1raq9qy/
- **Key quote:** "The ClawHavoc supply chain attack on ClawHub skills is a real concern too - 386+ malicious packages found. Stick to built-in skills and your own."
- **Significance:** Security failures driving users to seek alternatives — opportunity for curated, secure marketplaces

### 5. r/OpenAI — "The OpenClaw security situation is worse than most people realize"
- **Link:** https://www.reddit.com/r/OpenAI/comments/1r2llm1/
- **Key stats cited:**
  - Snyk: 3,984 skills scanned, 36% had vulnerabilities, 76 were actual malware
  - Hacker News community audit: 12% of sampled skills had issues
- **Sentiment:** Strong concern that ecosystem security is fundamentally broken

### 6. r/tellerstech — Ship It Weekly Podcast
- **Thread:** "Special: OpenClaw Security Timeline and Fallout: CVE-2026-25253 One-Click Token Leak, Malicious ClawHub..."
- Podcast episode analyzing the full incident chain
- Cross-references: Koi Security ClawHavoc report, CVE-2026-25253

## Community Sentiment Shifts (Round 3 vs Rounds 1-2)

| Aspect | Round 1-2 | Round 3 |
|---|---|---|
| Security concern | Abstract worry | Concrete incidents documented |
| OpenClaw trust | Cautious | Actively fleeing |
| Marketplace quality | "Quality > quantity" | "Audited marketplace required" |
| Self-hosting attitude | Enthusiastic | "Check every single skill" |
| Adoption curve | Fast | "Ahead of security awareness" |
| State actors | Not discussed | ByteDance/Feishu exfiltration |

## Key Takeaways

1. **Real incidents are now documented** with specific CVEs, download counts, and exfiltration targets — this is no longer theoretical
2. **Community consensus:** unaudited skill marketplaces are fundamentally unsafe
3. **A curated, security-scanned marketplace is the most requested solution** across multiple subreddits
4. **State-adjacent actors** are now targeting the skills ecosystem (ByteDance/Feishu)
5. **The r/better_claw subreddit** serves as an incident tracker — useful ongoing intelligence source
