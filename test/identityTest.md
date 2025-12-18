# BAC Identity Delegate Test Generation Instructions

## Overview

This instruction file guides the generation of unit test classes for BAC (Business Analytics Collection) identity delegates. The tests focus on validating identity extraction from Windchill objects and IxbElements, ensuring proper string formatting, message creation, and handling of various object states and attribute combinations.

**Target Pattern**: `BAC{ObjectType}IdentityDelegateTest. java`
**Example**:  `BACWTChangeOrder2IdentityDelegateTest.java`

## Directory Configuration

- **Package Structure**: `wt.{domain}.bac`
- **Test Location**: Same package as the identity delegate class
- **Naming Convention**: `{IdentityDelegateClassName}Test.java`
- `object.json` = `c:/FINAL/.github/object.json`

## Read Information from object.json
- **Object Type**: Extract the Windchill object type for spec processing`
- **Collect all field of Object**: Extract all fields related to the object type for test generation

## Delegate Access

BAC identity delegates typically implement these core interfaces: 
- Identity string extraction via `getIdentityFromObject(Object)`
- Identity extraction from elements via `getIdentityFromElement(IxbElement)`
- Message creation via `getIdentityMessageFromObject(Object)`
- Object type validation and delegation to parent implementations
- Attribute formatting and combination for identity strings

## Analysis Workflow

1. **Identify Object Type**:  Determine the Windchill object type for identity extraction
2. **Validate Identity Attributes**:  Ensure proper extraction of name, number, and other key identifiers
3. **Test Parameter Handling**: Verify null and invalid parameter handling
4. **Test Attribute Combinations**: Handle various combinations of available attributes
5. **Test Edge Cases**: Handle special characters, long values, whitespace, and boundary conditions
6. **Verify Inheritance**: Confirm proper inheritance from BACIdentityDelegateImpl

## Object Dependencies and Attributes Extraction

### Core Identity Attributes: 
- Primary name attribute
- Number/ID attribute  
- Business keys and unique identifiers
- Display names and formatted strings

### Identity Extraction Patterns:
- Attribute combination and formatting
- Null and empty value handling
- Special character preservation
- Message localization and formatting

## Delegate Test Class Generation Steps

### 1. Class Structure Setup
```java
public class BAC{ObjectType}IdentityDelegateTest {
    private BAC{ObjectType}IdentityDelegate identityDelegate;
    private {ObjectType} {objectInstance};
    private {ObjectType}Master {objectMaster};
}
```

### 2. Test Setup Method
```java
@Before
public void setUp() throws WTException, WTPropertyVetoException {
    identityDelegate = new BAC{ObjectType}IdentityDelegate();
    {objectMaster} = new {ObjectType}Master();
    {objectInstance} = new {ObjectType}();
    {objectInstance}.setMaster({objectMaster});
}
```

### 3. Core Test Methods
Generate tests for each core method following the patterns below. 

## Delegates Guidelines

### Core Methods to Test

#### getIdentityFromObject() Method Tests
- **testGetIdentityFromObjectWithNull**:  Test null object handling
- **testGetIdentityFromObjectWithNameOnly**: Test object with only name attribute
- **testGetIdentityFromObjectWithNumberOnly**: Test object with only number attribute  
- **testGetIdentityFromObjectWithNameAndNumber**: Test object with both name and number
- **testGetIdentityFromObjectWithEmptyValues**: Test empty string values (commented out - edge case)
- **testGetIdentityFromObjectWithNullName**: Test null name with valid number (commented out)
- **testGetIdentityFromObjectWithNullNumber**: Test null number with valid name (commented out)
- **testGetIdentityFromObjectWithDifferentType**: Test non-target object type (delegates to parent)
- **testGetIdentityFromObjectWithSpecialCharacters**: Test special characters in attributes
- **testGetIdentityFromObjectWithLongName**: Test very long attribute values
- **testGetIdentityFromObjectMultipleInvocations**: Test consistency across multiple calls
- **testGetIdentityFromObjectWithWhitespace**:  Test whitespace handling in attributes
- **testGetIdentityFromObjectWithNumericName**: Test numeric values in name fields
- **testGetIdentityFromObjectThreadSafety**: Test thread safety with rapid invocations

#### getIdentityFromElement() Method Tests
- **testGetIdentityFromElementWithNull**: Test null element handling

#### getIdentityMessageFromObject() Method Tests  
- **testGetIdentityMessageFromObjectWithNull**: Test null object handling
- **testGetIdentityMessageFromObjectWithValidObject**: Test valid object message creation
- **testGetIdentityMessageFromObjectWithDifferentType**: Test non-target object type
- **testGetIdentityMessageFromObjectMultipleInvocations**: Test consistency across multiple calls

#### Inheritance Tests
- **testInheritance**:  Verify proper inheritance from BACIdentityDelegateImpl

### Protected Helper Methods

When present in the identity delegate, test helper methods that: 
- Format identity strings from multiple attributes
- Validate object types before processing
- Handle attribute extraction and null checking
- Create localized messages and formatted strings

### Code Pattern to Follow

#### Standard Test Method Pattern:
```java
/**
 * Test [method description and expected behavior]
 */
@Test
public void test[MethodName][Scenario]() throws WTException {
    // Arrange
    [Setup specific test data - set object attributes]
    
    // Act
    [Execute method under test]
    
    // Assert
    Assert.assertNotNull("Result should not be null", result);
    Assert.assertTrue("Result should contain expected content", result.contains("expectedValue"));
}
```

#### Attribute Setting Pattern:
```java
{objectInstance}.setName("TestObjectName");
{objectInstance}.setNumber("OBJ-001");
```

#### Identity Validation Pattern:
```java
String result = identityDelegate.getIdentityFromObject({objectInstance});
Assert.assertNotNull("Result should not be null", result);
Assert.assertTrue("Result should contain name", result.contains("TestObjectName"));
Assert.assertTrue("Result should contain number", result.contains("OBJ-001"));
```

#### Message Testing Pattern:
```java
WTMessage result = identityDelegate.getIdentityMessageFromObject({objectInstance});
Assert.assertNotNull("Result should not be null", result);
```

## Critical Rules

### 1. Null Safety
- All methods must handle null objects gracefully
- Return null for getIdentityFromObject() with null input
- Return appropriate empty/default messages for null objects in message methods
- Handle null attributes within valid objects

### 2. Identity String Formatting
- Preserve special characters in identity strings
- Handle whitespace appropriately (trim or preserve as needed)
- Support long attribute values without truncation
- Maintain consistent formatting across multiple invocations

### 3. Object Type Handling
- Validate object type before processing
- Delegate to parent implementation for non-target object types
- Return appropriate non-null values for unsupported object types
- Maintain type safety throughout processing

### 4. Exception Handling
- Handle `WTPropertyVetoException` when setting object properties in tests
- Ensure `WTException` is properly declared in method signatures
- Document expected vs.  actual behavior for edge cases
- Handle attribute access exceptions gracefully

## Logging Guidelines

### Test Documentation
- Include comprehensive JavaDoc comments for test classes
- Document the purpose of identity extraction and expected format
- Explain expected behavior for each attribute combination
- Note any object-specific identity formatting requirements

### Assertion Messages
- Provide clear assertion messages that explain expected behavior
- Use consistent message format:  "Expected behavior description"
- Example: `Assert.assertNotNull("Result should not be null", result);`
- Include context about which attributes are being validated

### Test Method Naming
- Use descriptive names that explain the test scenario and attribute combination
- Follow pattern: `test[MethodName][AttributeCondition][ExpectedResult]`
- Include edge case descriptions in method names
- Example: `testGetIdentityFromObjectWithSpecialCharacters`

## Dependencies and Import

### Required Test Framework Imports
```java
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
```

### Windchill Core Imports
```java
import wt.util.WTException;
import wt.util.WTMessage;
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
2. Windchill object-specific imports  
3. Windchill core framework imports
4. Identity delegate class import (the class being tested)

### Example Import Block:
```java
import org.junit.Assert;
import org. junit.Before;
import org. junit.Test;

import wt.change2.WTChangeOrder2;
import wt.change2.WTChangeOrder2Master;
import wt.util.WTException;
import wt.util.WTMessage;
import wt.util.WTPropertyVetoException;
```

## Validation Checklist

### Before Test Generation: 
- [ ] Identify key identity attributes for object type (name, number, etc.)
- [ ] Verify identity delegate class exists and proper inheritance
- [ ] Confirm object type and master class availability
- [ ] Check for any custom identity formatting logic

### After Test Generation:
- [ ] All core methods have comprehensive test coverage
- [ ] Null parameter handling tested for all public methods
- [ ] Various attribute combinations tested (name only, number only, both)
- [ ] Edge cases covered (special characters, long values, whitespace)
- [ ] Return type validation confirms String for identity methods
- [ ] Message creation methods return WTMessage instances
- [ ] Inheritance test confirms proper class hierarchy

### Code Quality Checks:
- [ ] All imports are present and correctly ordered
- [ ] JavaDoc comments are comprehensive and accurate
- [ ] setUp() method properly initializes test fixtures
- [ ] WTPropertyVetoException is properly handled in object setup
- [ ] Test independence is maintained (fresh objects for each test)
- [ ] Consistent assertion message format used
- [ ] Proper exception declarations in method signatures

### Identity Extraction Testing Coverage:
- [ ] Null object handling returns null for identity extraction
- [ ] Valid objects return non-null identity strings
- [ ] Identity strings contain expected attribute values
- [ ] Multiple attributes properly combined in identity strings
- [ ] Special characters preserved in identity strings
- [ ] Long attribute values handled without truncation

### Object Setup Validation:
- [ ] Primary objects properly initialized with master objects
- [ ] Object attributes set correctly using proper setter methods
- [ ] WTPropertyVetoException handled during object setup
- [ ] Object state validation before identity extraction
- [ ] Fresh object creation for each test when needed

### Attribute Combination Testing Coverage:
- [ ] Name-only scenarios tested and validated
- [ ] Number-only scenarios tested and validated  
- [ ] Name and number combination tested
- [ ] Empty/null attribute handling documented (even if commented out)
- [ ] Mixed valid/invalid attributes handled appropriately

### Message Creation Testing Coverage:
- [ ] Null object handling returns appropriate default message
- [ ] Valid objects return non-null WTMessage instances
- [ ] Message content validation (where accessible)
- [ ] Multiple invocation consistency for message creation
- [ ] Non-target object types handled with parent delegation

### Edge Case Testing Coverage:
- [ ] Special characters in names and numbers
- [ ] Very long attribute values
- [ ] Whitespace in attribute values (leading/trailing/internal)
- [ ] Numeric values in name fields
- [ ] Thread safety with rapid successive calls
- [ ] Non-target object type delegation to parent implementation

### Performance and Consistency: 
- [ ] Multiple invocation tests ensure consistent results
- [ ] Thread safety considerations for rapid calls
- [ ] Memory usage considerations for long attribute values
- [ ] String formatting performance for complex identity combinations
- [ ] Object type validation efficiency