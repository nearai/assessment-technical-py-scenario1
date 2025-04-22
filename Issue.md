https://github.com/nearai/assessment-technical-ts-scenario1/issues/1

## User Story:
As a user with a specific task or question, I want to submit my query to an Agent Discovery System 
that intelligently matches me with the most suitable AI agent.

## Acceptance Criteria:
 * When I submit a natural language query to the system, it analyzes my request
* The system matches my query against a database of available agents with different specializations and capabilities
* I receive a recommendation of the top 3 most suitable agents for my specific query, with a brief explanation of why each was selected
* The system learns from successful and unsuccessful matches to improve future recommendations
* The entire matching process takes no more than 3 seconds from query submission to agent recommendations

## Technical Notes:
 * Our intern has used AI models to generate a partial implementation, the code in this repository.
     * It should run but has a few broken pieces that need to be fixed
 * The database already has up-to-date capability models for each available agent
 * We want a really great matching algorithm...
     * Matching algorithm should consider both semantic similarity and performance metrics
     * Then intern left ranking.ts as a placeholder for this functionality.
 * System should collect feedback after each session to improve future matching