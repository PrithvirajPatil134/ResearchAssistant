# Agentic Business Process Management: Practitioner Perspectives on Agent Governance in Business Processes

**Authors:** Hoang Vu (SAP), Nataliia Klievtsova (TU Munich), Henrik Leopold (Kuhne Logistics University), Stefanie Rinderle-Ma (TU Munich), Timotheus Kampik (SAP/Umea University)

**Source:** arXiv:2504.03693v2 | Conference paper, LNBIP vol. 565, pp. 29-43 (August 2025)

**Retrieved from:** https://arxiv.org/html/2504.03693v2

---

## Abstract

With the rise of generative AI, industry interest in software agents is growing. Given the stochastic nature of generative AI-based agents, their effective and safe deployment in organizations requires robust governance, which can be facilitated by agentic business process management. However, given the nascence of this new-generation agent notion, it is not clear what BPM practitioners consider to be an agent, and what benefits, risks and governance challenges they associate with agent deployments. To investigate how organizations can effectively govern AI agents, we conducted a qualitative study involving semi-structured interviews with 22 BPM practitioners from diverse industries. They anticipate that agents will enhance efficiency, improve data quality, ensure better compliance, and boost scalability through automation, while also cautioning against risks such as bias, over-reliance, cybersecurity threats, job displacement, and ambiguous decision-making. To address these challenges, the study presents six key recommendations for the responsible adoption of AI agents: define clear business goals, set legal and ethical guardrails, establish human-agent collaboration, customize agent behavior, manage risks, and ensure safe integration with fallback options. Additionally, the paper outlines actions to align traditional BPM with agentic AI, including balancing human and agent roles, redefining human involvement, adapting process structures, and introducing performance metrics. These insights provide a practical foundation for integrating AI agents into business processes while preserving oversight, flexibility, and trust.

---

## 1. Introduction

For over three decades, agents have periodically surged in Business Process Management (BPM). The 1990s saw early excitement around goal-oriented software agents, followed by the rise of Robotic Process Automation (RPA) in the late 2010s, promising efficiency gains for knowledge work. However, high initial expectations and maintenance costs led to mixed experiences in RPA adoption.

Large Language Model (LLM)-based agents fuel another wave of optimism. However, the stochastic nature of LLMs and related generative AI (genAI) technologies raises concerns, particularly regarding the need to govern the artifacts, decisions, and behaviors they produce. This prompts a critical question: how can BPM support the responsible integration of AI agents into organizations, ensuring both effective business outcomes and social accountability?

To explore this challenge from a practical perspective, we conducted interviews with BPM practitioners, capturing their insights on the potential implications of agents on organizations. The results reveal a dual landscape of opportunities and risks. On the one hand, practitioners anticipate benefits such as improved efficiency, predictive insights, and proactive decision-making. On the other hand, they express concerns about bias, over-reliance on automation, lack of transparency, and potential job displacement. This paper aims to address these concerns by providing recommendations practitioners should consider when introducing autonomous agents in business processes.

## 2. Background

### 2.1 Agents in Business Process Management

The integration of agent technologies into business process execution and coordination began in the early 1990s. An agent is typically defined as a computer program that "operates autonomously, perceives its environment, endures over time, adapts to change, and pursues goals" (Russell and Norvig, 2020, pp.21-22). In the context of Multi-Agent Systems (MAS), a business process can be viewed as a set of interacting agents coordinated by common organizational goals (Jennings et al., 1998, 2000); accordingly Agent-Oriented Programming (AOP) focuses, in its application proposals to BPM, primarily on business process execution (Jennings et al., 1996).

Over the decades, researchers have applied MAS to BPM to create more dynamic, cross-organizational processes while maintaining overall control. However, early implementations often faced challenges, including weak system control and issues with trust and delegation (Grundspenkis and Pozdnyakov, 2006).

In process modeling, process choreographies describe how independent agents coordinate by exchanging messages in a defined sequence and under specific conditions to accomplish a shared goal (Decker, 2009). Similarly, subject-oriented BPM shifts the focus from traditional process flows to subjects and their interactions, where subjects (e.g., humans, software, or agents) autonomously manage their tasks and decisions (Fleischmann et al., 2012).

With the rise of blockchain technologies, research further explored how networks of autonomous agents could underpin data sharing and decision logic through smart contracts (Mendling et al., 2018; Ladleif et al., 2019). In process analysis, agent-based methods have been developed for tasks such as process mining and simulation (Szimanski et al., 2013; Sulis and Taveter, 2022), including data-driven simulations that utilize event logs (Kirchdorfer et al., 2024). Agent System Mining (ASM) combines process mining with agent-based modeling to derive MAS models from real-world data (Tour et al., 2021, 2023; Shen et al., 2024). Reinforcement learning approaches have also been applied, enabling agents to test and refine different process variants through trial and error (Satyal et al., 2019; Kurz et al., 2024).

### 2.2 Robotic Process Automation

While agents and MAS address complex decision-making and coordination challenges, RPA aims to efficiently automate simple, rule-based tasks on a large scale. Since 2015, research on RPA has highlighted numerous examples of how business process automation can significantly enhance performance (Haase et al., 2024). When combined with BPM, RPA offers several advantages, including scalability, improved process accuracy, greater transparency and traceability, cost savings, and increased job satisfaction (Flechsig et al., 2019; Eulerich et al., 2024).

However, successfully applying RPA remains challenging, with 30-50% of initial projects failing during implementation (Hindle et al., 2017). While the primary causes of RPA failures result from technical limitations, there is also the problem of resistance against automation. Automated decision-making must comply with regulations, as the absence of human oversight can lead to legal and ethical risks. Even if successful, RPA is not suitable for full-scale business process automation as it focuses on automating repetitive tasks rather than orchestrating end-to-end processes (Konig et al., 2020).

### 2.3 Generative AI in Business Process Management

With the rise of LLMs, BPM researchers have begun exploring how these powerful tools can be integrated into business process management. Several studies (Vidgof et al., 2023; Bennoit et al., 2024; Buss et al., 2025) have examined all stages of the BPM lifecycle to identify areas where LLMs can add value. However, much of the current literature focuses on using LLMs from a conversational perspective, primarily addressing specific phases like discovery, analysis, and monitoring (Estrada-Torres et al., 2024).

In contrast, long-term visions of generative AI consider AI-based systems not merely as tools for task automation but as intelligent systems capable of adaptability, self-improvement, and bounded autonomy. Recent works (Dumas et al., 2023; Kampik et al., 2024; Rosemann et al., 2024) present AI-Augmented BPM Systems (ABPMSs) that enhance process execution, analysis, and optimization within structured workflows by supporting human decision-making rather than replacing it.

Despite these advances, a critical open question remains: How can BPM best support the management of increasingly autonomous software agents deployed in organizations, and what shifts in perspective are necessary to achieve this?

### 2.4 Agentic Business Process Management

Building on the research history of agents in BPM, RPA and generative AI in BPM, the authors introduce the concept of agentic Business Process Management (ABPM):

**Definition (Agentic Business Process Management):** Agentic Business Process Management (ABPM) describes (i) the deployment and execution of autonomous software agents to achieve business process goals and (ii) the application of agent-based abstractions for the process-oriented design and analysis of autonomous software agents.

Key concepts:
- An (autonomous) software agent is a computer program that "operates autonomously, perceives the environment, persists over a prolonged time period, adapts to change, and creates and pursues goals" (Russell and Norvig, 2020, pp.21)
- A process goal operationalizes the objective that an organization strives to achieve with the corresponding business process
- An agent-based abstraction is a conceptual model explicitly featuring notions of (software or human) agents
- Process-oriented design and analysis describes the modeling of business processes, as well as the drawing of inferences from data generated during process execution

The definition spans the key phases of the BPM lifecycle by addressing both deployment/execution and design/analysis.

## 3. Methodology

To explore how AI agents can be safely adopted in organizations and what the implications are for BPM, the authors utilized a qualitative research design and conducted in-depth interviews with experienced BPM practitioners.

**Research design:** The study uses a qualitative research design to examine the perspectives of professionals in business process management and automation, focusing on the integration and impact of agentic AI. It investigates the participants' understanding, expectations, and concerns related to agentic AI's autonomy, adaptability, human collaboration, and governance. The study also explores to what extent agent governance is required to address management needs that arise from greater software autonomy.

A qualitative content analysis approach (Mayring and Fenzl, 2019) was followed. Semi-structured interviews were conducted with professionals across various industries. The process began with transcription, familiarization with the interview data and analysis using a deductive-inductive coding approach. Initial deductive categories were derived from the research questions, while additional inductive subcategories emerged from the data.

The coding process:
1. Open coding: labeling segments of text with basic descriptive codes (e.g., benefits, risks, governance challenges)
2. Axial coding: grouping similar codes into broader categories (e.g., "automation potential" and "workflow optimization" to "benefits")
3. Selective coding: refining and integrating themes into a coherent framework

A total of 22 participants with experience with automation and AI technologies from various industries and roles were interviewed. Sessions lasted 60 to 90 minutes, with some conducted in pairs or groups due to accessibility constraints.

## 4. Results

### Understanding
Among the 22 participants, 10 were familiar with the term agentic AI, describing it as a self-learning technology that operates autonomously and adapts to its environment. Some viewed it as an evolution of RPA, overcoming technical limitations with AI. Others associated it with a digital assistant or an orchestration layer that coordinates tasks across specialized agents.

**Importantly, none of the participants reported having actual practical experience with agentic AI.** Assessments are based on expectations, often against the backdrop of existing agent-like automation technologies such as RPA.

### Benefits
Participants highlighted several potential benefits:
- Enhanced efficiency by automating routine tasks, reducing errors
- Improved data quality, ensuring consistent and accurate handling of information
- Better compliance, as agentic AI could monitor regulations and enforce standards automatically
- Scalability, enabling businesses to handle larger workloads without proportional staffing increases
- Democratization of process data, making it more accessible and usable

Participant quote: "More employees could initiate changes or optimizations if the software supports them directly, reducing dependency on specialized roles."

### Risks
Despite its potential, implementing agentic AI carries risks:
- Bias from flawed training data
- Over-reliance leading to diminished human judgment
- Lack of transparency in AI-driven decisions
- Cybersecurity threats
- Job displacement
- Unauthorized decision-making

Participant quote: "It's a cultural thing to be able to accept autonomy and decision making being taken away from a human."

### Use Cases
Key applications identified:
- Process monitoring to detect inefficiencies and suggest improvements
- Predictive analytics to forecast trends and provide actionable insights
- Task automation (data entry, document processing)
- Master data maintenance, user administration, root cause analysis
- Customer service enhancement
- Supply chain optimization (inventory management, demand prediction)
- Finance (fraud detection, transaction monitoring)
- Structuring unstructured datasets

Participant quote: "Processes often get stuck due to errors in master data, such as mismatched product codes or pricing issues. [Agentic] AI could analyze and fix these autonomously."

### Requirements
Participants stressed the need for:
- Clear rules and guidelines for ethical and transparent operation
- Audit logs, data retention, transparency, robust security
- Adherence to corporate policies and regulations
- Defined roles, responsibilities, and limitations
- Compliance with data protection laws and risk management frameworks
- Seamless integration with existing processes
- Comprehensive employee training
- Cost management (setup, maintenance, upgrades)
- Preconfigured use cases to build trust

Participant quote: "[The agent] would basically replace an FTE, let's just put it that way; you also have to provide it with the same framework that the employee would be confronted with because what would the employee do if they encounter difficulties?"

### Autonomy and Adaptability
- Human oversight essential for critical decisions or significant changes
- Configurable autonomy recommended: flexibility in low-risk areas, restriction in high-risk scenarios
- Gradual approach suggested: start with simple tasks, increase autonomy as trust grows
- Transparency essential: clear documentation of all AI decisions and actions
- High-level summaries for management, detailed logs for technical teams

Participant quote: "It shouldn't make changes in source systems or install new apps autonomously. That crosses the line because those areas are managed by different teams and require coordination."

Participant quote: "If it's routine, the decision itself should be documented. The more complex the task, the more I want to see how the process was developed."

### Human Involvement and Responsibility
- Agentic AI should serve as a decision-support tool for complex scenarios
- Should provide clear analyses, suggest actions, outline impacts
- Responsibility for failures is shared: organizations, developers, business leaders
- Organizations deploying agentic AI bear ultimate responsibility
- Key users and application owners identified as primary contacts for resolving issues
- Some suggested dedicated teams to manage accountability

Participant quote: "For complex decisions, the [agentic] AI should provide full context; how it arrived at the decision, what data it used, and the potential consequences; just like how humans consult colleagues for advice."

## 5. Recommendations for ABPM Adoption

### Six Critical Focus Areas

**1. Business context:** Organizations should define specific goals for the use of AI agents, clarify the expected benefits, and assess the short- and long-term costs associated with their deployment and maintenance.

**2. Guardrails:** Organizations must ensure that agents operate within the boundaries of legal, ethical, and organizational rules, while considering the context and environment in which the agents function.

**3. Human-agent collaboration:** Clear roles and responsibilities should be established to enable effective collaboration between humans and software agents, including identifying situations where human intervention is necessary in case of agent failure.

**4. Customization:** Organizations should tailor agents to meet their specific needs, determining factors such as the level of autonomy granted to agents, how human oversight and review are conducted, the extent of documentation required, and the desired level of reasoning and transparency in agent operations.

**5. Risk management:** Organizations must implement safety measures to monitor performance and address potential risks, including preventing undesired adaptability or evolution of the agents.

**6. Adoption:** Organizations must ensure the seamless and responsible integration of agents into existing business processes and systems, while implementing fallback mechanisms to enable a safe reversion if necessary.

### Four BPM Alignment Actions

**1. Human-agent balance:** Organizations should strive to design workflows that strategically use both AI capabilities and human expertise. This balance is essential for optimizing efficiency while preserving human judgment and creativity.

**2. Human involvement:** As intelligent agents become integral to business processes, organizations must clarify whether human actors will collaborate with agents as peers or take on supervisory roles with selective intervention.

**3. Process structures:** To fully realize the potential of self-adaptive agents, organizations should consider evolving beyond static process models and enabling more flexible, dynamic structures that can adjust in real time based on agent-driven insights.

**4. Performance metrics:** Effective integration of agentic AI requires clear metrics and performance indicators. Organizations should develop governance frameworks that track the impact of agents on process efficiency, decision quality, and broader organizational outcomes.

## 6. Limitations and Future Work

Several limitations:
- Sample was relatively small and predominantly drawn from experts at selected multinational organizations
- Concept of agentic AI remains in its formative stage; participants employed varied terminology
- Limited adoption and practical experience constrain interpretation of results

Future research should focus on:
- Refining and empirically validating the conceptual frameworks for agentic AI
- Particular emphasis on ethical, legal, and technical implications
- Quantitative studies and broader analyses across different industries
- Assessing the wider impact and evolution of agentic AI within various organizational contexts
- Developing robust governance structures ensuring transparent and accountable decision-making
- Examining how governance of agentic AI should differ from frameworks used for RPA

## 7. Conclusion

The rise of generative AI has sparked growing interest in its integration with software agents, giving rise to the concept of agentic AI. While this emerging technology holds promise, its impact on business processes and the requirements for its effective management remain insufficiently understood. This paper addresses this gap by identifying key recommendations for organizations seeking to implement AI agents responsibly.

Interviews with BPM practitioners reveal that next-generation software agents can enhance efficiency by automating routine tasks and allowing humans to focus on higher-value activities. At the same time, practitioners express concerns about risks such as bias, over-reliance, job displacement, and a lack of transparency. These concerns underscore the need for a clear governance framework to guide agent deployment.

Beyond implementation, the findings have broader implications for Business Process Management. Agentic AI introduces new dynamics (autonomy, adaptability, and self-learning) that challenge traditional BPM principles centered on structure, control, and standardization. To align these approaches, organizations should take strategic steps: design workflows that balance human and agent input, redefine human roles as collaborators or supervisors, evolve static process models to support adaptive agent behavior, and implement metrics and governance frameworks to monitor performance and outcomes.

---

## References

[1] Multiagent systems: a modern approach to distributed artificial intelligence. MIT Press (1999)
[2] Bennoit, C., Greff, T., Baum, D., Bajwa, I.A.: Identifying use cases for large language models in the business process management lifecycle. In: 2024 26th International Conference on Business Informatics (CBI). pp. 256-263. IEEE (2024)
[3] Berti, A., Maatallah, M., Jessen, U., Sroka, M., Ghannouchi, S.A.: Re-thinking process mining in the AI-based agents era (2024)
[4] Buss, A., Kratsch, W., Schmid, S.J., Wang, H.: ProcessLLM: A LLM specialized in the interpretation, analysis, and optimization of business processes. In: Business Process Management Workshops. Springer (2025)
[5] Decker, G.: Design and analysis of process choreographies. Ph.D. thesis, Universitat Potsdam (2009)
[6] Dumas, M., Fournier, F., Limonad, L., Marrella, A., Montali, M., Rehse, J., Accorsi, R., Calvanese, D., Giacomo, G.D., Fahland, D., Gal, A., Rosa, M.L., Volzer, H., Weber, I.: AI-augmented business process management systems: A research manifesto. ACM Trans. Manag. Inf. Syst. 14(1), 11:1-11:19 (2023)
[7] Estrada-Torres, B., del-Rio-Ortega, A., Resinas, M.: Mapping the landscape: Exploring LLM applications in business process management. In: Enterprise, Business-Process and Information Systems Modeling. pp. 22-31 (2024)
[8] Eulerich, M., Waddoups, N., Wagener, M., Wood, D.A.: The dark side of robotic process automation (RPA): Understanding risks and challenges with RPA. Accounting Horizons 38(2), 143-152 (2024)
[9] Flechsig, C., Lohmer, J., Lasch, R.: Realizing the full potential of robotic process automation through a combination with BPM. Logistics Management (2019)
[10] Fleischmann, A., Schmidt, W., Stary, C., Obermeier, S., Borger, E.: Subject-oriented business process management. Springer Nature (2012)
[11] Grundspenkis, J., Pozdnyakov, D.: An overview of the agent based systems for the business process management (2006)
[12] Haase, J., Kremser, W., Leopold, H., Mendling, J., Onnasch, L., Plattfaut, R.: Interdisciplinary directions for researching the effects of robotic process automation and large language models on business processes. Communications of the Association for Information Systems 54, 579-604 (2024)
[13] Hindle, J., Lacity, M., Willcocks, L., Khan, S.: Robotic process automation. Tech. rep., Interim Executive Research Report (2017)
[14] Jennings, N.R., Faratin, P., Johnson, M.J., Norman, T.J., O'Brien, P.D., Wiegand, M.E.: Agent-based business process management. Int. J. Cooperative Inf. Syst. 5(2&3), 105-130 (1996)
[15] Jennings, N.R., Norman, T.J., Faratin, P.: ADEPT: an agent-based approach to business process management. SIGMOD Rec. 27(4), 32-39 (1998)
[16] Jennings, N.R., Norman, T.J., Faratin, P., O'Brien, P.D., Odgers, B.: Autonomous agents for business process management. Appl. Artif. Intell. 14(2), 145-189 (2000)
[17] Kampik, T., Warmuth, C., Rebmann, A., Agam, R., Egger, L., Gerber, A., Hoffart, J., Kolk, J., Herzig, P., Decker, G., van der Aa, H., Polyvyanyy, A., Rinderle-Ma, S., Weber, I., Weidlich, M.: Large process models: A vision for business process management in the age of generative AI. KI - Kunstliche Intelligenz (2024)
[18] Kirchdorfer, L., Blumel, R., Kampik, T., Van der Aa, H., Stuckenschmidt, H.: AgentSimulator: An agent-based approach for data-driven business process simulation. In: 2024 6th Int. Conf. on Proc. Mining (ICPM). pp. 97-104. IEEE (2024)
[19] Kurz, A.F., Kampik, T., Pufahl, L., Weber, I.: Business process improvement with AB testing and reinforcement learning: grounded theory-based industry perspectives. Software and Systems Modeling (2024)
[20] Konig, M., Bein, L., Nikaj, A., Weske, M.: Integrating Robotic Process Automation into Business Process Management, pp. 132-146 (2020)
[21] Ladleif, J., Weske, M., Weber, I.: Modeling and enforcing blockchain-based choreographies. In: Business Process Management. pp. 69-85 (2019)
[22] Mayring, P., Fenzl, T.: Qualitative Inhaltsanalyse, pp. 633-648. Springer (2019)
[23] Mendling, J., et al.: Blockchains for business process management - challenges and opportunities. ACM Trans. Manag. Inf. Syst. 9(1), 4:1-4:16 (2018)
[24] OMG: Business Process Model and Notation (BPMN), Version 2.0 (January 2011)
[25] Rosemann, M., Brocke, J.v., Van Looy, A., Santoro, F.: Business process management in the age of AI - three essential drifts. Information Systems and e-Business Management 22, 1-15 (2024)
[26] Russell, S.J., Norvig, P.: Artificial Intelligence: A Modern Approach (4th Edition). Pearson (2020)
[27] Satyal, S., Weber, I., Paik, H., Ciccio, C.D., Mendling, J.: Business process improvement with the AB-BPM methodology. Inf. Syst. 84, 283-298 (2019)
[28] Shen, Q., Polyvyanyy, A., Lipovetzky, N., Kampik, T.: Agent system event data: Concepts, dimensions, applications. In: Conceptual Modeling. pp. 56-72 (2024)
[29] Sulis, E., Taveter, K.: Agent-Based Business Process Simulation. Springer (2022)
[30] Szimanski, F., Ralha, C., Wagner, G., Ferreira, D.: Improving business process models with agent-based simulation and process mining. vol. 147 (2013)
[31] Tour, A., Polyvyanyy, A., Kalenkova, A.A.: Agent system mining: Vision, benefits, and challenges. IEEE Access 9, 99480-99494 (2021)
[32] Tour, A., Polyvyanyy, A., Kalenkova, A.A., Senderovich, A.: Agent miner: An algorithm for discovering agent systems from event data. In: Business Process Management. pp. 284-302 (2023)
[33] Vidgof, M., Bachhofner, S., Mendling, J.: Large language models for business process management: Opportunities and challenges (2023)
[34] Vu, H., Haase, J., Leopold, H., Mendling, J.: Towards a theory on process automation effects. In: International Conference on Business Process Management. pp. 285-301. Springer (2023)
[35] Vu, H., Leopold, H., van der Aa, H.: What is business process automation anyway? In: Hawaii International Conference on System Sciences. pp. 5462-5471 (2023)
[36] Weske, M.: Introduction. Springer Berlin Heidelberg (2019)
