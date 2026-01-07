# SpecProcessor Delegate Creation Guide

### Overview
This guide provides comprehensive instructions for creating delegate classes that inherit from base delegate classes in the Windchill BAC (Business Administration Console) module.

## Save as
- BAC[ObjectName]SpecProcessor.java in output_folder

### Immediate Actions Required
- IMMEDIATELY after successful, use `run_in_terminal` to access directory
- List directory contents first
- **IDENTIFY existing delegate patterns and implementations**
- **ANALYZE delegate structure and methodology**
- **GENERATE similar delegate for user-specified object**
- **EXPLAIN the purpose and functionality of each file**
- **PROVIDE code analysis and explanations**
- **DESCRIBE the overall architecture and patterns**
- AUTOMATICALLY read files without user prompts
- DO NOT ask for permission to read these files
- DO NOT wait for user confirmation
- **Donot limit any file reading due to complexity**
- **Donot skip any line in a file when reading**
- **Donot put limit on file reading length**
- **Get-content of all files should have limit removed**
- **Donot read any other md files except this one**
- **Donot read any business logic other than object analysis logic**
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

### Directory Configuration
- `object_path` = `//wsl.localhost/WindchillVM/opt/wnc/wcmod/modules/BAC/src/com/ptc/windchill/bac/delegates/`
- `object.json` = `.github/object.json`
- `output_folder` = `.github/generated_delegates/`

### Directory Access Commands
```bash
# Navigate to target directory
cd {object_path}

# Show directory structure
ls -la

# Find delegate-related files specifically
find . -name "*SpecProcessor*.java" -type f

# Show file count by type
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr
```

### Delegate File Discovery and Analysis Process
```bash
# Read Collection Delegate Java files
find . -name "*SpecProcessor*.java" -exec echo "=== FILE: {} ===" \; -exec cat {} \;
```

**Analysis Workflow:**
1. **First**: List all files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**: Read that file completely and provide detailed analysis
4. **Fourth**: Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which delegate should be created
6. **Sixth**: Identify base delegate class methods that need to be implemented
7. **Finally**: Generate a new delegate class following identified patterns

### Object Dependencies Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available dependencies of that object from `object.json`

### Delegate Class Generation Steps
1. **First**: Create a new Java class file named `BAC[Template_Name]SpecProcessor.java`
2. **Second**: Ask user which base delegate to extend from
3. **Third**: Implement core methods 
4. **Fourth**: Include necessary imports and package declarations
5. **Fifth**: Add proper logging using Log4j2 Logger
6. **Sixth**: Create protected helper methods following base delegate patterns
7. **Seventh**: **Generate minimal business logic - focus on structure and method signatures**
8. **Finally**: Save the generated file in `output_folder`

### Delegate Guidelines (Based on BACSpecProcessor Pattern)

#### Class Structure
- **Package**: `[directory].bac`
- **Implements**: `BACSpecProcessor` interface
- **Logger**: Use Log4j2 Logger: `LogR.getLoggerInternal(YourClassName.class.getName())`
- **Collection Category**: Use appropriate enum from `CollectionCategory` which is uppercase of object name

#### Core Methods to Implement
- **Constructor**
- **process(BACSpec spec, ArrayList<BACCollectionSpec> specList, ArrayList<BACRawCollectionSpec> rawSpecList)**

#### Code Patterns to Follow
- **Constructor**
```java
public BAC[Template_Name]SpecProcessor() {
    setCollnCategory(CollectionCategory.[Template_Name]);
}
```

**Collection Category:**
```java
CollectionCategory TEMPLATE_UPPERCASE = toCollectionCategory("Template");
return CollectionCategory.TEMPLATE_UPPERCASE;
```

- **process Method**
```java
@Override
public void process(com.ptc.windchill.bac.specfile.jaxb.BACSpec spec, ArrayList<BACCollectionSpec> specList, ArrayList<BACRawCollectionSpec> rawSpecList) throws WTException {
    if(spec.get[Template_Name]() ==null)
            return;

    BACCollectionSpec collnSpec = new BACCollectionSpec(CollectionCategory.[Template_Name]);

    BACRawCollectionSpec rawCollnSpec = new BACRawCollectionSpec(CollectionCategory.[Template_Name]);
}
``` 
- **getCollnCategory Method** --> no override
```java
    public CollectionCategory getCollnCategory() {
        return collnCategory;
    }
 ```

- **setCollnCategory Method** --> no override
```java
    protected void setCollnCategory(CollectionCategory collnCategory) {
        this.collnCategory = collnCategory;
    }
 ```

### Critical Rules
- DO NOT add any more method than specified above
- if there is any method that is not specified above, add it as a comment with TODO for business logic
- Donot implement any business logic that is not specified above
- Donot read any other file after user provide a specific file name to read
- Donot create any super class method if it is not specified above
- Donot create any additional helper methods unless specified above 

### Logging Guidelines
- Debug level: Method entry/exit, collection sizes, important variables
- Trace level: Detailed object content (use sparingly)
- Info level: Missing configurations, important state changes
- Error level: Exceptions and error conditions

### Dependencies and Imports
```java
import org.apache.logging.log4j.Logger;
import com.ptc.windchill.bac.*;
import wt.fc.PersistenceHelper;
import wt.fc.collections.*;
import wt.log4j.LogR;
import wt.query.QuerySpec;
import wt.util.WTAttributeNameIfc;
import wt.util.WTException;
import com.ptc.windchill.bac.delegates.BACSpecProcessor;
```
### Import ant Statements
- Use proper import statements for all classes used in the delegate
- Ensure no unused imports are present
- Follow Windchill coding standards for import organization

### Business Logic Guidelines
- **Minimal implementation**: Focus on structure and query patterns
- **Use TODO comments** for complex business logic
- **Reference base delegate methods** for standard operations
- **Ask user for clarification** on domain-specific logic
- **Keep delegates generic** for easy extension
- **Suggest business logic approach** in TODO comments without implementing

### Validation Checklist
Before finalizing the generated delegate:
- [ ] Extends correct base delegate class
- [ ] Implements all required interface methods
- [ ] Contains proper package declaration
- [ ] Includes all necessary imports
- [ ] Has Logger instance correctly configured
- [ ] Protected fields are properly declared
- [ ] Query patterns match base delegate approach
- [ ] Date range filtering is correctly implemented
- [ ] Null checks are in place
- [ ] Debug logging is added at key points
- [ ] TODO comments mark uncertain business logic

