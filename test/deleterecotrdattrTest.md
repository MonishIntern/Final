# BAC Delete Record Attributes Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) delete record attributes classes. The tests focus on validating identity attribute extraction and management for deleted Windchill objects, ensuring proper handling of delete records and attribute mapping.

**Target Pattern**: `BAC{ObjectType}DeleteRecordAttributesTest. java`
**Example**:  `BACWTChangeOrder2DeleteRecordAttributesTest. java`

## Directory Configuration

- **Package Structure**: `wt. {domain}. bac`
- **Test Location**: Same package as the delete record attributes class
- **Naming Convention**: `{DeleteRecordAttributesClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC delete record attributes classes typically implement these core interfaces: 
- Identity attribute extraction via `getIdentityAttributesWithValues(BACGenericDeleteRecord)`
- Attribute mapping and transformation
- Delete record validation and processing
- Collection category-specific attribute handling

## Analysis Workflow

1. **Identify Object Type**: Determine the Windchill object type for delete record processing
2. **Validate Attribute Mapping**: Ensure proper identity attribute extraction
3. **Test Parameter Handling**: Verify null and invalid parameter handling
4. **Test Data Integrity**: Validate attribute values and ordering
5. **Verify Return Types**:  Confirm `LinkedHashMap<String, String>` return types
6. **Test Edge Cases**: Handle special characters, long values, and boundary conditions

## Object Dependencies and Attributes Extraction

### Core Identity Attributes to Consider:
- Primary identifiers (name, number, ID)
- Business keys and unique identifiers
- Parent-child relationship identifiers
- Version-specific attributes

### Delete Record Patterns:
- Attribute extraction from delete records
- Value transformation and formatting
- Order preservation in attribute maps
- Category-specific attribute handling

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}DeleteRecordAttributesTest {
    private BAC{ObjectType}DeleteRecordAttributes deleteRecordAttributes;
    private BACGenericDeleteRecord deleteRecord;
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() {
    deleteRecordAttributes = new BAC{ObjectType}DeleteRecordAttributes();
    deleteRecord = new BACGenericDeleteRecord();
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below. 

## Delegates Guidelines

### Core Methods to Test

#### Constructor Tests
- **testConstructor**: Verify proper initialization of delete record attributes instance

#### getIdentityAttributesWithValues() Method Tests
- **testGetIdentityAttributesWithNullDeleteRecord**: Test null delete record handling
- **testGetIdentityAttributesWithValidDeleteRecord**: Test valid delete record processing
- **testGetIdentityAttributesPreservesOrder**:  Verify LinkedHashMap ordering preservation
- **testGetIdentityAttributesWithSpecialCharacters**: Test special character handling
- **testGetIdentityAttributesMultipleInvocations**: Test consistency across multiple calls
- **testGetIdentityAttributesReturnsNonNullMap**:  Verify non-null return guarantee
- **testGetIdentityAttributesWithLongName**: Test handling of long attribute values
- **testGetIdentityAttributesWithDifferentCategory**: Test different collection category handling
- **testGetIdentityAttributesThreadSafety**: Test thread safety and rapid invocations

#### Inheritance Tests
- **testInheritance**: Verify proper inheritance from BACDeleteRecordAttributes

### Protected Helper Methods

When present in the delete record attributes class, test helper methods that:
- Transform attribute values
- Validate delete record data
- Handle category-specific logic
- Format attribute strings

### Code Pattern to Follow

#### Standard Test Method Pattern: 
```java
/**
 * Test [method description and expected behavior]
 */
@Test
public void test[MethodName][Scenario]() throws WTPropertyVetoException {
    // Arrange
    [Setup test data - delete record with attributes]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    [Additional assertions for expected behavior]
}
```

#### Delete Record Setup Pattern:
```java
deleteRecord.setName("TestObjectName");
deleteRecord.setCollectionCategory(CollectionCategory.{OBJECT_TYPE});
```

#### Attribute Validation Pattern:
```java
Assert.assertTrue("Result should contain expected key", result.containsKey("expectedKey"));
Assert.assertEquals("Value should match", expectedValue, result.get("expectedKey"));
```

#### Order Verification Pattern:
```java
Assert.assertTrue("Result should be LinkedHashMap type", result instanceof LinkedHashMap);
```

## Critical Rules

### 1. Null Safety
- All methods must handle null delete records gracefully
- Return empty LinkedHashMap for null inputs (never return null)
- Validate delete record state before attribute extraction
- Handle missing or null attribute values appropriately

### 2. Return Type Consistency
- `getIdentityAttributesWithValues()` must return `LinkedHashMap<String, String>`
- Preserve insertion order using LinkedHashMap
- Never return null - return empty map when no attributes found
- Ensure consistent key naming conventions

### 3. Data Integrity
- Preserve original attribute values without unwanted transformation
- Handle special characters and Unicode properly
- Support long attribute values without truncation
- Maintain attribute value type consistency (all String values)

### 4. Exception Handling
- Handle `WTPropertyVetoException` in test methods that set delete record properties
- Use appropriate exception declarations in method signatures
- Test both successful and error scenarios
- Document expected exception behavior

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document the purpose of identity attribute extraction
- Explain expected attribute mappings and transformations
- Note any category-specific behavior or special cases

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:  "Expected behavior description"
- Example: `Assert.assertNotNull("Result should not be null", result);`
- Include context about which attributes are being validated

### Test Method Naming
- Use descriptive names that explain the test scenario
- Follow pattern: `test[MethodName][Condition][ExpectedResult]`
- Include edge case descriptions in method names
- Example: `testGetIdentityAttributesWithSpecialCharacters`

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org. junit.Before;
import org.junit.Test;
```

### Java Collections Imports
```java
import java.util.LinkedHashMap;
```

### BAC Framework Imports
```java
import com.ptc.windchill. bac.BACGenericDeleteRecord;
import com.ptc.windchill.bac. CollectionCategory;
```

### Windchill Core Imports
```java
import wt.util.WTPropertyVetoException;
```

### Object-Specific Imports
Import the specific Windchill object type if needed:
```java
import wt.{domain}.{ObjectType};
```

## Import Statements

### Standard Import Order: 
1. Java standard library imports (java.util. *)
2. JUnit framework imports
3. BAC framework imports
4. Windchill core framework imports
5. Domain-specific object imports
6. Delete record attributes class import (the class being tested)

### Example Import Block:
```java
import java.util.LinkedHashMap;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import com.ptc.windchill.bac.BACGenericDeleteRecord;
import com. ptc.windchill.bac.CollectionCategory;

import wt.util.WTPropertyVetoException;
```

## Validation Checklist

### Before Test Generation: 
- [ ] Identify correct CollectionCategory enum value for object type
- [ ] Verify delete record attributes class exists and is accessible
- [ ] Confirm inheritance from BACDeleteRecordAttributes
- [ ] Check for any custom identity attributes specific to object type

### After Test Generation:
- [ ] Constructor test validates proper initialization
- [ ] All core methods have corresponding tests
- [ ] Null parameter handling is tested comprehensively
- [ ] Valid delete record scenarios are covered
- [ ] Return type validation confirms LinkedHashMap usage
- [ ] Order preservation is tested and verified

### Code Quality Checks:
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes test fixtures
- [ ] WTPropertyVetoException is properly handled in tests
- [ ] Test independence is maintained (no shared state)
- [ ] Consistent assertion message format used
- [ ] Proper exception declarations in method signatures

### Identity Attribute Testing Coverage:
- [ ] Null delete record handling tested
- [ ] Valid delete record with standard attributes tested
- [ ] Special character handling in attribute values tested
- [ ] Long attribute value handling tested
- [ ] Multiple invocation consistency tested
- [ ] Different collection category handling tested
- [ ] Thread safety considerations tested

### Data Integrity Testing Coverage:
- [ ] Attribute value preservation verified
- [ ] Order preservation in LinkedHashMap confirmed
- [ ] Non-null return guarantee tested
- [ ] Empty map return for invalid input tested
- [ ] Attribute key naming consistency verified

### Edge Case Testing Coverage:
- [ ] Special characters in attribute values
- [ ] Very long attribute values
- [ ] Empty string attribute values
- [ ] Different collection categories
- [ ] Rapid successive method invocations
- [ ] Inheritance relationship verification

### Delete Record Setup Patterns:
- [ ] Proper delete record initialization in setUp()
- [ ] Consistent attribute setting patterns
- [ ] Appropriate collection category assignment
- [ ] Exception handling for property setting operations