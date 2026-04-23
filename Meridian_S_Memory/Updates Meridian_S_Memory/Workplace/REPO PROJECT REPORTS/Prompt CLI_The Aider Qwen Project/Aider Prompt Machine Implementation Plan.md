---
modified: 2026-04-19T05:31:05+03:00
---
Prompt Machine Implementation Plan                                                                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


Task 1: Project Structure & Initialization                                                                                   

Files to create:                                                                                                             

 • prompt_cli/__init__.py                                                                                                    
 • prompt_cli/main.py                                                                                                        
 • prompt_cli/config.py                                                                                                      
 • prompt_cli/utils.py                                                                                                       

Purpose: Set up basic project structure and entry point.                                                                     

Key functions:                                                                                                               

 • main() - Entry point function                                                                                             
 • get_config_dir() - Returns ~/.prompt-cli/ path                                                                            
 • ensure_directories() - Creates required directories                                                                       


Task 2: Template Management System                                                                                           

Files to modify: prompt_cli/main.py, add new file prompt_cli/templates.py                                                    

Purpose: Handle template storage, retrieval, and listing.                                                                    

Key functions:                                                                                                               

 • create_template_dir() - Initialize ~/.prompt-cli/templates/                                                               
 • list_templates() - List all available templates                                                                           
 • save_template(name, content) - Save template to file                                                                      
 • load_template(name) - Load template from file                                                                             


Task 3: Variable Injection Engine                                                                                            

Files to modify: Add new file prompt_cli/injector.py                                                                         

Purpose: Parse templates and inject variables based on {{variable_name}} syntax.                                             

Key functions:                                                                                                               

 • extract_variables(template_content) - Extract variable names from template                                                
 • inject_variables(template_content, variables_dict) - Replace placeholders with values                                     
 • prompt_for_variables(variables_list) - Interactive input for missing variables                                            


Task 4: Configuration Management                                                                                             

Files to modify: prompt_cli/config.py                                                                                        

Purpose: Manage application configuration including API keys, default models, etc.                                           

Key functions:                                                                                                               

 • load_config() - Load config from ~/.prompt-cli/config.json                                                                
 • save_config(config_data) - Save configuration                                                                             
 • get_api_key() - Retrieve API key from config or environment                                                               
 • set_default_model(model_name) - Set default model in config                                                               


Task 5: API Integration Layer                                                                                                

Files to modify: Add new file prompt_cli/api.py                                                                              

Purpose: Handle communication with Alibaba Cloud Model Studio API.                                                           

Key functions:                                                                                                               

 • send_to_alibaba_api(prompt, model) - Send processed prompt to API                                                         
 • format_request_body(prompt, model) - Prepare API request payload                                                          
 • handle_api_response(response) - Process and return API response                                                           


Task 6: Command-Line Interface Setup                                                                                         

Files to modify: prompt_cli/main.py                                                                                          

Purpose: Implement CLI commands using argparse/click for all operations.                                                     

Key functions:                                                                                                               

 • setup_cli_parser() - Configure command-line arguments                                                                     
 • run_command(args) - Execute requested operation based on args                                                             
 • Subcommands: create, list, run, config, init                                                                              


Task 7: Git Integration for Version Control                                                                                  

Files to modify: prompt_cli/utils.py, add new file prompt_cli/git_handler.py                                                 

Purpose: Initialize and manage Git repository for tracking template changes.                                                 

Key functions:                                                                                                               

 • init_git_repo() - Initialize Git repo in config directory                                                                 
 • commit_template_changes(filename, message) - Commit template modifications                                                
 • check_git_status() - Verify Git is available and repo exists                                                              
 • auto_commit_on_change() - Auto-commit template updates                                                                    


Task 8: Main Execution Flow                                                                                                  

Files to modify: prompt_cli/main.py                                                                                          

Purpose: Integrate all components into cohesive workflow.                                                                    

Key functions:                                                                                                               

 • execute_template_run(template_name, model, variables) - Complete execution flow                                           
 • interactive_mode() - Handle interactive template execution                                                                
 • validate_prerequisites() - Check Git, config, API access before running                                                   


Task 9: Error Handling & Validation                                                                                          

Files to modify: All files for comprehensive error handling                                                                  

Purpose: Ensure robust error handling throughout the application.                                                            

Key functions:                                                                                                               

 • validate_template_syntax(content) - Validate template format                                                              
 • handle_api_errors(exception) - Handle API-related errors gracefully                                                       
 • validate_model_name(model) - Verify supported model names                                                                 
 • config_validation() - Validate configuration integrity                                                                    


Task 10: Installation & Packaging                                                                                            

Files to create: setup.py, README.md, requirements.txt                                                                       

Purpose: Make the CLI tool installable via pip with proper dependencies.                                                     

Key components:                                                                                                              

 • setup.py with entry point for prompt-cli command                                                                          
 • Requirements: requests, gitpython, click or argparse                                                                      
 • Installation instructions in README                                                                                       


Tokens: 438 sent, 926 received.

litellm.NotFoundError: OpenAIException - The model `qwen3-coder-turbo` does not exist or you do not have access to it.