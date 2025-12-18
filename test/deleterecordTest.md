# BAC Delete Record Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) delete record classes. The tests focus on validating delete record creation, attribute management, and proper handling of Windchill object references for deleted objects.

**Target Pattern**: `BAC{ObjectType}DeleteRecordTest. java`
**Example**:  `BACWTChangeOrder2DeleteRecordTest.java`

## Directory Configuration

- **Package Structure**: `wt.{domain}.bac`
- **Test Location**: Same package as the delete record class
- **Naming Convention**: `{DeleteRecordClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC delete record classes typically implement these core interfaces: 
- Delete record creation via `new{ObjectType}DeleteRecord(ObjectReference, BACDeleteInfo)`
- Name management via `getName()` and `setName(String)`
- String representation via `toString()`
- Attribute extraction and management
- Object reference handling and validation

## Analysis Workflow

1. **Identify Object Type**: Determine the Windchill object type for delete record creation
2. **Validate Object Setup**:  Ensure proper test object initialization with required attributes
3. **Test Factory Methods**:  Verify delete record creation through factory methods
4. **Test Attribute Management**: Validate name and other attribute handling
5. **Test Edge Cases**:  Handle null parameters, special characters, and boundary conditions
6. **Verify Inheritance**: Confirm proper inheritance from BACDeleteRecord

## Object Dependencies and Attributes Extraction

### Core Object Components:
- Primary Windchill object (e.g., WTChangeOrder2)
- Master object (e.g., WTChangeOrder2Master)
- ObjectReference for the primary object
- BACDeleteInfo for deletion metadata

### Object Attribute Patterns:
- Name attribute extraction and management
- Number/ID attribute handling
- Object reference creation and validation
- Master object relationship setup

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}DeleteRecordTest {
    private {ObjectType} {objectInstance};
    private ObjectReference objectReference;
    private BACDeleteInfo deleteInfo;
    private {ObjectType}Master {objectMaster};
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() throws Exception {
    // Create test object
    {objectInstance} = new {ObjectType}();
    {objectMaster} = new {ObjectType}Master();
    {objectInstance}.setMaster({objectMaster});
    {objectInstance}.setName("Test{ObjectType}");
    
    // Create object reference
    objectReference = ObjectReference.newObjectReference({objectInstance});
    
    // Create delete info
    deleteInfo = new BACDeleteInfo();
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below. 

## Delegates Guidelines

### Core Methods to Test

#### Factory Method Tests
- **testNew{ObjectType}DeleteRecord**:  Test successful delete record creation
- **testNewDeleteRecordWithNullReference**: Test null object reference handling (expected exception)
- **testNewDeleteRecordWithNullDeleteInfo**: Test null delete info handling (expected exception)
- **testMultipleDeleteRecordCreation**: Test creating multiple delete records from same source

#### Attribute Management Tests
- **testGetName**: Test name retrieval from delete record
- **testSetName**: Test name modification functionality
- **testDeleteRecordWithNumber**: Test object with number/ID attributes
- **testDeleteRecordWithSpecialCharacters**: Test special character handling in names
- **testDeleteRecordWithLongName**: Test handling of long attribute values

#### String Representation Tests
- **testToString**: Test string representation includes expected content

#### Inheritance Tests
- **testDeleteRecordInheritance**:  Verify proper inheritance from BACDeleteRecord

### Protected Helper Methods

When present in the delete record class, test helper methods that:
- Extract attributes from object references
- Transform object data to delete record format
- Validate object state before delete record creation
- Handle object-specific attribute mapping

### Code Pattern to Follow

#### Standard Test Method Pattern: 
```java
/**
 * Test [method description and expected behavior]
 */
@Test
public void test[MethodName][Scenario]() throws WTException {
    // Arrange
    [Setup specific test data]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    [Additional assertions for expected behavior]
}
```

#### Factory Method Test Pattern:
```java
@Test
public void testNew{ObjectType}DeleteRecord() throws WTException {
    BAC{ObjectType}DeleteRecord deleteRecord = 
        BAC{ObjectType}DeleteRecord.new{ObjectType}DeleteRecord(objectReference, deleteInfo);
    
    Assert.assertNotNull("Delete record should not be null", deleteRecord);
    Assert.assertEquals("Name should match", expectedName, deleteRecord.getName());
}
```

#### Exception Test Pattern:
```java
@Test(expected = Exception.class)
public void testNew{ObjectType}DeleteRecordWithNull[Parameter]() throws WTException {
    BAC{ObjectType}DeleteRecord. new{ObjectType}DeleteRecord([null parameter], [valid parameter]);
}
```

#### Object Setup Pattern:
```java
{objectInstance}. setName("TestName");
{objectInstance}.setNumber("OBJ-001");
objectReference = ObjectReference.newObjectReference({objectInstance});
```

## Critical Rules

### 1. Object Initialization
- Always create proper master objects for Windchill objects that require them
- Set required attributes (name, number, etc.) before creating object references
- Handle WTPropertyVetoException properly when setting object properties
- Create fresh ObjectReference instances for modified objects

### 2. Exception Handling
- Use `@Test(expected = Exception.class)` for null parameter tests
- Handle `WTPropertyVetoException` when setting object properties
- Ensure `WTException` is properly declared in method signatures
- Use try-catch blocks with proper logging for property setting operations

### 3. Factory Method Testing
- Test the static factory method `new{ObjectType}DeleteRecord()`
- Verify non-null return values from factory methods
- Test with both valid and invalid parameters
- Ensure multiple invocations create separate instances

### 4. Attribute Validation
- Verify name extraction works correctly
- Test name modification through setName()
- Validate special character handling in attributes
- Test boundary conditions (empty names, long names)

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document the purpose of delete record creation and management
- Explain expected behavior for each test scenario
- Note any object-specific requirements or constraints

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:  "Expected behavior description"
- Example: `Assert.assertNotNull("Delete record should not be null", deleteRecord);`
- Include context about which attributes are being validated

### Exception Handling in Tests
- Use TODO comments for auto-generated exception handling blocks
- Log exception details when appropriate for debugging
- Document expected vs.  actual exception behavior
- Handle WTPropertyVetoException consistently across tests

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org. junit.Before;
import org. junit.Test;
```

### BAC Framework Imports
```java
import com.ptc.windchill. bac.BACDeleteInfo;
```

### Windchill Core Imports
```java
import wt.fc.ObjectReference;
import wt.util.WTException;
import wt.util.WTPropertyVetoException;
```

### Object-Specific Imports
Import the specific Windchill object type and its master: 
```java
import wt.{domain}.{ObjectType};
import wt.{domain}.{ObjectType}Master;
```

## Import Statements

### Standard Import Order: 
1. JUnit framework imports
2. BAC framework imports
3. Windchill object-specific imports
4. Windchill core framework imports
5. Delete record class import (the class being tested)

### Example Import Block:
```java
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.ptc.windchill. bac.BACDeleteInfo;

import wt.change2.WTChangeOrder2;
import wt.change2.WTChangeOrder2Master;
import wt.fc.ObjectReference;
import wt.util.WTException;
import wt.util.WTPropertyVetoException;
```

## Validation Checklist

### Before Test Generation:
- [ ] Identify correct Windchill object type and its master class
- [ ] Verify delete record class exists and has appropriate factory method
- [ ] Confirm required object attributes for proper initialization
- [ ] Check inheritance from BACDeleteRecord

### After Test Generation:
- [ ] Factory method tests validate successful creation
- [ ] Null parameter tests use appropriate expected exceptions
- [ ] Object setup properly initializes master objects
- [ ] Name and attribute management tests are comprehensive
- [ ] toString() method test validates content inclusion
- [ ] Inheritance test confirms proper class hierarchy

### Code Quality Checks:
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes all test fixtures
- [ ] WTPropertyVetoException is properly handled in object setup
- [ ] Test independence is maintained (fresh object creation)
- [ ] Consistent assertion message format used
- [ ] Proper exception declarations in method signatures

### Object Setup Validation:
- [ ] Primary object properly initialized with required attributes
- [ ] Master object created and associated with primary object
- [ ] ObjectReference creation handled correctly
- [ ] BACDeleteInfo properly initialized
- [ ] Object modifications create fresh ObjectReference instances

### Factory Method Testing Coverage:
- [ ] Successful creation with valid parameters tested
- [ ] Null object reference parameter throws exception
- [ ] Null delete info parameter throws exception
- [ ] Multiple creation invocations create separate instances
- [ ] Factory method returns correct delete record type

### Attribute Management Testing Coverage:
- [ ] Name retrieval works correctly
- [ ] Name modification through setName() tested
- [ ] Special characters in names handled properly
- [ ] Long names processed without truncation
- [ ] Number/ID attributes handled when present
- [ ] Empty or null name scenarios covered (if applicable)

### Edge Case Testing Coverage:
- [ ] Special characters in object names
- [ ] Very long object names
- [ ] Objects with additional attributes (numbers, descriptions)
- [ ] Multiple delete record creation from same source
- [ ] toString() method includes expected information
- [ ] Inheritance relationship verification

### Exception Handling Validation:
- [ ] WTPropertyVetoException properly caught and handled
- [ ] Expected exceptions properly declared in test annotations
- [ ] Exception handling includes appropriate logging/comments
- [ ] Error scenarios are covered without breaking test flow