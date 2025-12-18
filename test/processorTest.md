# BAC Delete Processor Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) delete processors.  The tests focus on validating delete operations for Windchill objects, ensuring proper parameter handling, object identification, and delete processing workflows.

**Target Pattern**: `BAC{ObjectType}DeleteProcessorTest. java`
**Example**:  `BACWTChangeOrder2DeleteProcessorTest.java`

## Directory Configuration

- **Package Structure**: `wt.{domain}.bac`
- **Test Location**: Same package as the delete processor class
- **Naming Convention**: `{DeleteProcessorClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC delete processors typically implement these core interfaces: 
- Object identification via `findByIdentityParams(List<Map<String, String>>)`
- Object type identification via `getObjType()` and `getObjSelector()`
- Delete processing via `processDelete(Collection, Object, boolean)`
- Skip processing via `processSkip(Collection)`
- Conflict resolution via `getConflictElements(Object, List<Map<String, String>>)`
- Main delete workflow via `delete(Object, List<Map<String, String>>)`

## Analysis Workflow

1. **Identify Object Type**:  Determine the Windchill object type being processed for deletion
2. **Validate Parameter Handling**:  Ensure proper handling of null and empty parameters
3. **Test Object Identification**: Verify identity parameter lookup functionality
4. **Test Delete Operations**: Validate delete and skip processing methods
5. **Verify Return Types**:  Confirm proper return types for all methods
6. **Test Exception Handling**: Verify proper exception handling and graceful degradation

## Object Dependencies and Attributes Extraction

### Core Object Attributes to Consider:
- Identity parameters (name, number, ID)
- Object references and relationships
- State information for delete eligibility
- Dependency chains that might block deletion

### Delete Processing Patterns:
- Parameter-based object lookup
- Conflict detection and resolution
- Bulk delete operations
- Skip processing for non-deletable objects

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}DeleteProcessorTest {
    private BAC{ObjectType}DeleteProcessor deleteProcessor;
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() {
    deleteProcessor = new BAC{ObjectType}DeleteProcessor();
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below. 

## Delegates Guidelines

### Core Methods to Test

#### findByIdentityParams() Method Tests
- **testFindByIdentityParamsWithNullInput**:  Test null parameter list handling
- **testFindByIdentityParamsWithEmptyList**: Test empty parameter list handling
- **testFindByIdentityParamsWithSingleParam**: Test single parameter map processing
- **testFindByIdentityParamsWithMultipleParams**: Test multiple parameter maps processing

#### getObjType() Method Tests
- **testGetObjType**:  Verify correct object type string return

#### getObjSelector() Method Tests
- **testGetObjSelector**: Verify correct selector string return
- **testGetObjSelectorWithObject**: Test selector with object parameter
- **testGetObjSelectorWithNullObject**: Test selector with null object parameter

#### processSkip() Method Tests
- **testProcessSkipWithEmptyCollection**: Test empty collection handling
- **testProcessSkipWithNullCollection**: Test null collection handling (expected exception)

#### processDelete() Method Tests
- **testProcessDeleteWithEmptyCollection**: Test empty collection handling
- **testProcessDeleteWithNullCollection**:  Test null collection handling (if applicable)

#### getConflictElements() Method Tests
- **testGetConflictElementsWithNullInput**: Test null parameter handling
- **testGetConflictElementsWithEmptyParams**:  Test empty parameter list handling

#### delete() Method Tests
- **testDeleteWithNullRequest**: Test null request handling
- **testDeleteWithEmptyParams**: Test empty parameter list handling
- **testDeleteWithNullParams**: Test null parameter list handling

### Protected Helper Methods

When present in the delete processor, test helper methods that: 
- Validate input parameters
- Transform parameter maps to query criteria
- Handle specific object type deletion logic
- Process dependency chains

### Code Pattern to Follow

#### Standard Test Method Pattern: 
```java
/**
 * Test [method description and expected behavior]
 */
@Test
public void test[MethodName][Scenario]() throws WTException {
    // Arrange
    [Setup test data - parameter maps, collections, etc.]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    [Additional assertions for expected behavior]
}
```

#### Exception Test Pattern:
```java
@Test(expected = [SpecificException]. class)
public void test[MethodName]With[ErrorCondition]() throws WTException {
    [deleteProcessor].[method]([invalid parameters]);
}
```

#### Parameter Map Creation Pattern:
```java
List<Map<String, String>> paramList = new ArrayList<>();
Map<String, String> params = new HashMap<>();
params.put("name", "TestObjectName");
params.put("number", "OBJ-001");
paramList.add(params);
```

## Critical Rules

### 1. Parameter Handling
- All methods must handle null parameters gracefully
- Empty parameter lists should be processed without errors
- Invalid parameter formats should be handled appropriately
- Return empty collections rather than null when no results found

### 2. Return Type Consistency
- `findByIdentityParams()` must return `Map<Object, WTReference>`
- `getObjType()` and `getObjSelector()` must return `String`
- `getConflictElements()` must return `List`
- Never return `null` - return empty collections/maps instead

### 3. Exception Handling
- Use specific exception types in `@Test(expected = ...)` annotations
- Ensure `WTException` is properly declared in method signatures
- Test both expected exceptions and graceful handling scenarios
- Document expected vs. actual exception behavior

### 4. Collection Handling
- Test with empty collections
- Test with null collections (where exceptions are expected)
- Test with populated collections containing test objects
- Verify proper iteration and processing

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document the purpose of each test method
- Explain expected behavior vs. actual implementation status
- Note any stub implementations that need future updates

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:  "Expected behavior description"
- Example: `Assert.assertNotNull("Result should not be null", result);`
- Include context about what the test is validating

### Implementation Notes
- Add TODO comments for tests that need updates when implementation is complete
- Document any assumptions about current stub behavior
- Note expected changes when full implementation is available

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org. junit.Before;
import org. junit.Test;
```

### Java Collections Imports
```java
import java.util.ArrayList;
import java. util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
```

### Windchill Core Imports
```java
import wt.fc.WTReference;
import wt.fc. collections.WTArrayList;
import wt.util.WTException;
```

### Object-Specific Imports
Import the specific Windchill object type being tested:
```java
import wt.{domain}.{ObjectType};
```

## Import Statements

### Standard Import Order: 
1. Java standard library imports (java.util. *)
2. JUnit framework imports
3. Windchill core framework imports
4. Domain-specific object imports
5. Delete processor class import (the class being tested)

### Example Import Block:
```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import wt.change2.WTChangeOrder2;
import wt.fc.WTReference;
import wt.fc.collections.WTArrayList;
import wt. util.WTException;
```

## Validation Checklist

### Before Test Generation:
- [ ] Identify correct object type and domain
- [ ] Verify delete processor class exists and is accessible
- [ ] Confirm object type import availability
- [ ] Check for any custom parameter requirements

### After Test Generation:
- [ ] All core methods have corresponding tests
- [ ] Null parameter handling is tested for all public methods
- [ ] Empty collection/parameter handling is tested
- [ ] Return types are validated in tests
- [ ] Exception handling tests use appropriate expected exceptions
- [ ] Parameter map creation follows consistent patterns
- [ ] Test method names are descriptive and follow naming conventions

### Code Quality Checks:
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes test fixtures
- [ ] No hardcoded values that should be parameterized
- [ ] Test independence is maintained (no shared state)
- [ ] Consistent assertion message format used
- [ ] Proper exception declarations in method signatures

### Parameter Testing Coverage:
- [ ] Null input testing for all methods accepting parameters
- [ ] Empty collection/list testing where applicable
- [ ] Single parameter map testing
- [ ] Multiple parameter map testing
- [ ] Invalid parameter format handling (if applicable)

### Delete Process Testing Coverage:
- [ ] Object identification testing via identity parameters
- [ ] Object type and selector method testing
- [ ] Skip processing functionality testing
- [ ] Delete processing functionality testing
- [ ] Conflict detection and resolution testing
- [ ] Main delete workflow testing with various scenarios

### Implementation Status Awareness:
- [ ] Tests account for current implementation status (stub vs. complete)
- [ ] TODO comments added for future implementation updates
- [ ] Expected behavior documented even if not yet implemented
- [ ] Test assertions appropriate for current implementation level