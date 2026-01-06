# ExpImpFor[ObjectName] Delegate Creation Guide

### Overview
This guide provides comprehensive instructions for creating delegate classes that inherit from base delegate classes in the Windchill BAC (Business Administration Console) module.

## Save as
- ExpImpFor[ObjectName].java in output_folder

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
- `object.json` = `.github/object.json`
- `IXL_handler_path` = `//wsl.localhost/WindchillVM/opt/wnc/Windchill/DevModules/IXLoad/src/wt/`

**Analysis Workflow:**
1. **First**: List all files from above commands output
2. **Second**: Ask user which file to read first from the list
3. **Third**: Read that file completely and provide detailed analysis
4. **Fourth**: Repeat steps 2 and 3 until all files are analyzed
5. **Fifth**: After reading all files, ask user for the Object for which delegate should be created
6. **Sixth**: Generate a new delegate class following identified patterns

### Object Attributes Extraction and Selection
1. **First**: After user provides object name, search for that object in `object.json` file from `.github/object.json`
2. **Second**: Display all available attributes of that object from `object.json`
3. **Third**: Ask user to select which attributes to include in the generated delegate

### Delegate Class Generation Steps
1. **First**: Create a new Java class file named `ExpImpFor[ObjectName].java`
2. **Second**: Implement core methods 
3. **Third**: Include necessary imports and package declarations
4. **Fourth**: Add proper logging using Log4j2 Logger
5. **Fifth**: Create protected helper methods following base delegate patterns
6. **Sixth**: **Generate minimal business logic - focus on structure and method signatures**
7. **Finally**: Save the generated file in `output_folder`

### Delegate Guidelines (Based on ExpImpFor[ObjectName] Pattern)

#### Class Structure
- **Package**: `directory`
- **Implements**: `ExpImpFor[ObjectName]` interface
- **Logger**: Use Log4j2 Logger: `LogR.getLoggerInternal(YourClassName.class.getName())`

#### Class Description
- extends `_ExpImpFor[ObjectName]`
- Annotation `@ExportableType(handlerType = "Class", className = [ObjectName].class, generateCode = false, superClass = ExpImpForVersionableChangeItem.class, rootTag = "[ObjectName]")`

#### Core Methods to Implement
- **getRootTag()**
- **getObjectClassName()**
- **getObjectMasterClassName()**
- **prepareForExport(WTCollection objsToExport, Exporter exporter)**
- **exportObjectSpecificAttributes(Object object, IxbElement fileXML, Exporter exporter)**
- **checkConflicts(List<IxbElement> fileXMLs, Importer importer)**
- **importObjectsAttributes(List<ElementObjectPair> elementObjectPairs, Importer importer)**
- **importObjectsAttributesAfterStore(List<ElementObjectPair> elementObjectPairs, Importer importer)**
- **getIxbObjectRef()**
- **createNewObject(IxbElement fileXML, Importer importer)**
- **createEmptyObject(IxbElement fileXML, Importer importer, Mastered master)** (optional)

#### Code Patterns to Follow
- **Logger Setup**
```java
private static final Logger logger = LogR.getLoggerInternal(ExpImpFor[ObjectName].class.getName());

// Optional: Profile prefix for performance monitoring
private static final String IMPORT_PROFILE_PREFIX;
static {
    final String simpleName = ExpImpFor[ObjectName].class.getSimpleName() + "_";
    IMPORT_PROFILE_PREFIX = "IMPORT_PROFILE_PREFIX_" + simpleName;
}
```

- **getRootTag** 
```java
@Override
protected String getRootTag() {
    return IxbHndHelper.XML_[OBJECTNAME];
}
```

- **getObjectClassName Method**
```java
@Override
public String getObjectClassName() {
    return [ObjectName].class.getName();
}
```

- **getObjectMasterClassName Method**
```java
@Override
public String getObjectMasterClassName() {
    return [ObjectName]Master.class.getName();
}
```

- **prepareForExport Method**
```java
@Override
public void prepareForExport(WTCollection objsToExport, Exporter exporter) throws WTException {
    super.prepareForExport(objsToExport, exporter);
    // Add specific attribute preparations if needed
    AttributeExporterImporter attrEI = exporter.attributeExporterImporterManager
            .getAttributeExporterImporter(ExpImpFor[ObjectName]Attr.class);
    attrEI.prepareAttributeForExport(objsToExport, exporter);
}
```

- **exportObjectSpecificAttributes Method**
```java
@Override
protected void exportObjectSpecificAttributes(Object object, IxbElement fileXML, Exporter exporter) throws WTException {
    IxbHndHelper.exportAttribute(ExpImpFor[ObjectName]Attr.class, object, fileXML, exporter);
    // Add additional attribute exports as needed
}
```

- **checkConflicts Method**
```java
@Override
public void checkConflicts(final List<IxbElement> fileXMLs, final Importer importer) throws WTException {
    try (ProfilePoint pp = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "checkConflicts_all")) {
        try (ProfilePoint pp1 = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "checkConflicts_super")) {
            super.checkConflicts(fileXMLs, importer);
        }
        
        try (ProfilePoint pp1 = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "checkConflicts_local")) {
            final List<ElementObjectPair> objectPairs = getFileXMLObjectPairs(fileXMLs, importer);
            IxbHndHelper.checkConflictForAttributeBatch(ExpImpFor[ObjectName]Attr.class, objectPairs, importer, this);
        }
    }
}
```

- **importObjectsAttributes Method**
```java
@Override
public List<ElementObjectPair> importObjectsAttributes(List<ElementObjectPair> objectPairs, Importer importer) throws WTException {
    try (ProfilePoint pp = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "importObjectsAttributes_all")) {
        try (ProfilePoint pp1 = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "importObjectsAttributes_super")) {
            objectPairs = super.importObjectsAttributes(objectPairs, importer);
        }
        
        try (ProfilePoint pp1 = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "importObjectsAttributes_local")) {
            IxbHndHelper.importAttributeBatch(ExpImpFor[ObjectName]Attr.class, objectPairs, importer);
            return objectPairs;
        }
    }
}
```

- **importObjectsAttributesAfterStore Method**
```java
@Override
public List<ElementObjectPair> importObjectsAttributesAfterStore(List<ElementObjectPair> objectPairs,
        final Importer importer) throws WTException {
    try (ProfilePoint pp = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "importObjectsAttributesAfterStore_all")) {
        try (ProfilePoint pp1 = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "importObjectsAttributesAfterStore_super")) {
            objectPairs = super.importObjectsAttributesAfterStore(objectPairs, importer);
        }
        
        try (ProfilePoint pp1 = ProfilePoint.profileAction(IMPORT_PROFILE_PREFIX + "importObjectsAttributesAfterStore_common")) {
            // Add specific attribute processing if needed
            return objectPairs;
        }
    }
}
```

- **getIxbObjectRef Method**
```java
@Override
protected String getIxbObjectRef() {
    return IxbHndHelper.XML_[OBJECTNAME]_REF;
}
```

- **createNewObject Method**
```java
@Override
public Versioned createNewObject(IxbElement fileXML, Importer importer) throws WTException {
    logger.debug("creating new [objectname].");
    return [ObjectName].new[ObjectName]();
}
```

- **createEmptyObject Method (Optional)**
```java
@Override
public Versioned createEmptyObject(IxbElement fileXML, Importer importer, Mastered master) throws WTException {
    Versioned object = [ObjectName].new[ObjectName]();
    logger.debug("creating new [objectname] with master.");
    try {
        object.setMaster(master);
    } catch (WTPropertyVetoException e) {
        throw new WTException(e);
    }
    return object;
}
```

### Critical Rules
- DO NOT add any methods other than those specified above
- If there are additional methods needed, add them as comments with TODO for business logic
- Do not implement any business logic that is not specified above
- Do not read any other file after user provides a specific file name to read
- Do not create any super class methods if not specified above
- Do not create any additional helper methods unless specified above
- Use ProfilePoint for performance monitoring in import/export operations
- Always call super methods first in overridden methods
- Use proper exception handling with WTException
- Implement proper logging with debug level for method entry/exit 

### Logging Guidelines
- Use Log4j2 Logger: `LogR.getLoggerInternal(ClassName.class.getName())`
- Debug level: Method entry/exit, object creation, important state changes
- Info level: Important configuration or processing information
- Error level: Exceptions and error conditions
- Use ProfilePoint for performance monitoring in critical import/export operations
- Follow consistent naming for profile actions: `IMPORT_PROFILE_PREFIX + methodName + "_section"`

### Dependencies and Imports
```java
import java.util.List;

import org.apache.logging.log4j.Logger;

import wt.facade.ixb.IxbElement;
import wt.facade.ixb.profile.ProfilePoint;
import wt.fc.collections.WTCollection;
import wt.ixb.publicforapps.Exporter;
import wt.ixb.publicforapps.Importer;
import wt.ixb.publicforhandlers.AttributeExporterImporter;
import wt.ixb.publicforhandlers.IxbHndHelper;
import wt.ixb.publicforhandlers.IxbHndHelper.ElementObjectPair;
import wt.log4j.LogR;
import wt.util.WTException;
import wt.util.WTPropertyVetoException;
import wt.vc.Mastered;
import wt.vc.Versioned;

import com.ptc.windchill.annotations.handlerAutomationMetadata.ExportableType;

// Object-specific imports
import [package].[ObjectName];
import [package].[ObjectName]Master;
import [package].ixb.attr.ExpImpFor[ObjectName]Attr;
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
- [ ] Extends correct base delegate class `_ExpImpFor[ObjectName]`
- [ ] Implements all required methods from the interface
- [ ] Contains proper package declaration
- [ ] Includes all necessary imports
- [ ] Has Logger instance correctly configured with LogR.getLoggerInternal
- [ ] Contains @ExportableType annotation with correct parameters
- [ ] Uses ProfilePoint for performance monitoring in import/export methods
- [ ] Calls super methods appropriately in overridden methods
- [ ] Proper exception handling with WTException
- [ ] Debug logging is added at key points
- [ ] Attribute export/import patterns match base delegate approach
- [ ] Object creation methods return correct types (Versioned)
- [ ] Master object handling is implemented if needed
- [ ] TODO comments mark uncertain business logic

