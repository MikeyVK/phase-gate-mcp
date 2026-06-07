# **Architectuurgids: Strikt Workflow-beheer voor Custom Agents via MCP**

## **1\. Context & Doelstelling**

Het doel is het dwingend opleggen van de operationele context aan gerichte GitHub Copilot custom agents (@co, @imp, @qa). Hierbij fungeert de output van de MCP (Model Context Protocol) tool get\_work\_context als de absolute bron van waarheid (*single source of truth*) waaraan de agents gedurende de workflow moeten gehoorzamen.

## **2\. Implementatiestrategieën**

### **2.1 Systeem-prompt Conditionering**

De basisinstructies (systeem-prompts) van de custom agents moeten de informatiehiërarchie expliciet vastleggen. De tool-respons dient boven de standaard prompt-instructies of het interne modelgeheugen te worden geplaatst.

**Op te nemen restricties in de agent-configuratie:**

* **Initiële Blokkade:** De agent mag geen code genereren, andere tools aanroepen of acties uitvoeren voordat get\_work\_context succesvol is uitgevoerd en geanalyseerd.  
* **Informatiehiërarchie:** Instructies, fase-bepalingen en restricties in de respons van get\_work\_context overschrijven te allen tijde het standaardgedrag van de agent.

### **2.2 Gestructureerde Tool-Respons (XML-Schema)**

LLM's reageren nauwkeuriger op strikte afbakening. Door de output van get\_work\_context in XML te structureren, wordt de semantische interpretatie door de agent gestandaardiseerd.

\<work\_context\>  
  \<current\_phase\>Implementation\</current\_phase\>  
  \<active\_agent\>@imp\</active\_agent\>  
  \<strict\_constraints\>  
    \<constraint\>Je mag uitsluitend bestanden wijzigen in de /src/components directory.\</constraint\>  
    \<constraint\>Test-driven development (TDD) is verplicht: schrijf geen implementatiecode zonder een corresponderende falende test of test-status te verifiëren.\</constraint\>  
  \</strict\_constraints\>  
  \<allowed\_tools\>  
    \<tool\>read\_file\</tool\>  
    \<tool\>write\_file\</tool\>  
    \<tool\>run\_tests\</tool\>  
  \</allowed\_tools\>  
\</work\_context\>

### **2.3 Server-side Phase-Gating (Harde Handhaving)**

Om deterministische striktheid te garanderen, mag de handhaving niet uitsluitend afhankelijk zijn van de compliantie van het taalmodel. De MCP-server moet actieve state-validatie uitvoeren.

* **Validatie op Serverniveau:** Als een agent (bijv. @imp) een tool aanroept die buiten de huidige geautoriseerde fase valt (bijv. write\_file tijdens de coördinatiefase), weigert de MCP-server de executie.  
* **Foutafhandeling:** De server retourneert een expliciete foutmelding die de agent dwingt zijn status te heroverwegen:  
  ERROR: Action denied by Phase-Gate. Current phase allows only coordination operations. Call get\_work\_context to review the active constraints.

### **2.4 Procedurele Validatie (Chain of Thought)**

Dwing het model via de systeem-prompt of tool-instructie om de actieve restricties eerst verbaal te verwerken alvorens tot actie over te gaan. Dit activeert het procedurele redeneervermogen van het model.

* **Context Check:** De agent moet elke response verplicht starten met een kort logisch blok (\<context\_check\>) waarin de actieve fase en de geldende restricties uit de laatst opgehaalde werkcontext worden bevestigd.

## **3\. Workflow-Overzicht**

1. **User Prompt** ![][image1] Activeert Custom Agent (@co / @imp / @qa).  
2. **Verplichte Tool Call** ![][image1] Agent roept get\_work\_context aan op de MCP-server.  
3. **State Delivery** ![][image1] Server retourneert gestructureerde XML met restricties en toegestane tools.  
4. **Execution & Gatekeeping** ![][image1] Agent voert taken uit binnen de marges. Bij overschrijding blokkeert de MCP-server de tool-aanroepen via server-side phase-gating.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAAAt0lEQVR4XmNgGAWjgDpAQUGBQ05OLk1UVJQHXY4cwCgvL98KNNAYXYIsADIIaGAvkMmCLkcOYAR6twBoaByIjSIDlBAA2iRJClZSUgKaJTcfyJ6soqLCBzZIXFycGyhQDcSzSMVAw3YA6a9A3Aw0kB3FhaQAWVlZE6Ahq6WlpWXQ5UgCQAOEgQYtVlRUlEeXIxkADcoChnMEujjJAJRogYZNlZGRkUaXIwcwqqur84JodIlRMMAAAJV7J+RoCL8jAAAAAElFTkSuQmCC>