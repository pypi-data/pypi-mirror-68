#!/usr/bin/env python3
"""A script that converts the mulitple inputs of a function to a single
Params Autovalue class.

Usage: python3 sorno_input_params_autovalue_converter.py sample_function_defs.txt --output_autovalue_class

Usage: python3 sorno_input_params_autovalue_converter.py sample_function_defs.txt --convert_method_calls_in_test_file sample_convert_method_calls_in_test_file.txt

Usage: python3 sorno_input_params_autovalue_converter.py sample_function_defs.txt --convert_call_site_file sample_convert_call_site_file.txt

    Copyright 2020 Heung Ming Tai
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import argparse

import re
import sys
import subprocess
from collections import namedtuple


fields = ('type', 'name', 'default_value')
Param = namedtuple('Param', fields, defaults=(None,) * len(fields))

AUTO_VALUE_CLASS_NAME = 'Params'

AUTO_VALUE_GET_METHOD_TEMPLATE = 'public abstract {type} {method_name}();'

AUTO_VALUE_SET_METHOD_TEMPLATE = 'public abstract Builder {method_name}({type} {param_name});'
AUTO_VALUE_CLASS_TEMPLATE = """\
import com.google.auto.value.AutoValue;

/** Input parameters for {func_name}. */
@AutoValue
public abstract static class Params {{
  {get_methods_defs}

  public static Builder builder() {{
      // TODO
      return new AutoValue_Params.Builder(){build_default_calls};
  }}

  abstract Builder toBuilder();

  /** Builder for {{@link Params}} */
  @AutoValue.Builder
  public abstract static class Builder {{
    {set_methods_defs}

    public abstract Params build();
  }}
}}
"""


class App(object):
    def __init__(self, args):
      self.args = args
      self.func_def_input_file = args.func_def_input_file

    def run(self):
      func_def_str = open(self.func_def_input_file).read()
      func_name = get_func_name(func_def_str)
      params = get_params(func_def_str)

      if self.args.output_autovalue_class:
        print_autovalue_class(func_name, params)

      if self.args.convert_method_calls_in_test_file:
        content = open(self.args.convert_method_calls_in_test_file).read()
        print(replace_content_for_test_file(func_name, params, content))

      if self.args.convert_call_site_file:
        content = open(self.args.convert_call_site_file).read()
        print(replace_content_for_call_site_file(func_name, params, content))

      return 0


def get_func_name(s):
  pre_open_paren_str = s.split('(')[0]
  if ' ' not in pre_open_paren_str:
    return pre_open_paren_str

  return pre_open_paren_str[pre_open_paren_str.rindex(' ') + 1:]


def get_params(s):
  post_open_paren_str = s.split('(', 1)[1]
  params_str = get_until_close_paren(post_open_paren_str)
  params_strs = [s.strip() for s in params_str.split(',')]

  params = []
  for param_str in params_strs:
    # Need to prevent the case that the type and parameter names are separated
    # by newlines or more than one spaces, so replace all whitespaces to
    # single space.
    param_fragments = re.sub(r'\s+', ' ', param_str).split(' ')
    t, param_name = param_fragments[-2], param_fragments[-1]
    if t == 'Boolean':
      t = 'boolean'

    if t == 'boolean':
      param = Param(type=t, name=param_name, default_value='false')
    else:
      param = Param(type=t, name=param_name)

    params.append(param)

  return params


def get_until_close_paren(s):
  open_paren_count = 0
  for i in range(len(s)):
    c = s[i]
    if c == ')':
      if open_paren_count:
        open_paren_count -= 1
      else:
        return s[:i]
    elif c == '(':
      open_paren_count += 1

  # no idea what to do, so just return s
  return s


def print_autovalue_class(func_name, params):
  get_methods_defs_strs = []
  set_methods_defs_strs = []
  build_default_calls_strs = []
  for param in params:
    get_methods_defs_strs.append(AUTO_VALUE_GET_METHOD_TEMPLATE.format(
        type=param.type,
        method_name=param.name,
    ))

    set_method_name = 'set' + upperfirst(param.name)
    set_methods_defs_strs.append(AUTO_VALUE_SET_METHOD_TEMPLATE.format(
        method_name=set_method_name,
        type=param.type,
        param_name=param.name,
    ))

    if param.default_value:
      build_default_calls_strs.append('.{set_method_name}({value})'.format(
          set_method_name=set_method_name,
          value=param.default_value,
      ))

  get_methods_defs = '\n'.join(['\n  ' + s for s in get_methods_defs_strs])
  set_methods_defs = '\n'.join(['\n    ' + s for s in set_methods_defs_strs])

  build_default_calls = ''.join(['\n    ' + s for s in build_default_calls_strs])

  print(AUTO_VALUE_CLASS_TEMPLATE.format(
      func_name=func_name,
      get_methods_defs=get_methods_defs,
      set_methods_defs=set_methods_defs,
      build_default_calls=build_default_calls,
  ))


def upperfirst(s):
  return s[0].upper() + s[1:]


def replace_content_for_test_file(func_name, params, content):
  func_name_anchor = '.' + func_name + '('
  output = ""
  while func_name_anchor in content:
    # E.g. "abcd blah.func(f1, f2, f3) hello"
    # is splitted to "abcd blah" and "f1, f2, f3) hello"
    pre, post = content.split(func_name_anchor, 1)

    # E.g. "f1, f2, f3"
    input_args_str = get_until_close_paren(post)
    replaced_input_args = replace_test_input_args_with_autovalue_class(input_args_str, params)
    output += pre + func_name_anchor + replaced_input_args
    content = post[len(input_args_str):]

  # need to append the remaining content which does not have the func name
  # anchor
  output += content

  return output


def replace_content_for_call_site_file(func_name, params, content):
  func_name_anchor = '.' + func_name + '('
  output = ""
  while func_name_anchor in content:
    # E.g. "abcd blah.func(f1, f2, f3) hello"
    # is splitted to "abcd blah" and "f1, f2, f3) hello"
    pre, post = content.split(func_name_anchor, 1)

    # E.g. "f1, f2, f3"
    input_args_str = get_until_close_paren(post)
    replaced_input_args = replace_input_args_with_autovalue_class(input_args_str, params)
    output += pre + func_name_anchor + replaced_input_args
    content = post[len(input_args_str):]

  # need to append the remaining content which does not have the func name
  # anchor
  output += content

  return output


def replace_test_input_args_with_autovalue_class(input_args_str, params):
  input_arg_strs = input_args_str.split(',')
  output = AUTO_VALUE_CLASS_NAME + ".builder()"
  cleaned_arg_strs = [clean_input_arg(s) for s in input_arg_strs]

  for arg, param in zip(cleaned_arg_strs, params):
    if can_skip_arg(arg):
      continue
    output += "\n.set%s(%s)" % (upperfirst(param.name), arg)
  output += "\n.build()"
  return output


def replace_input_args_with_autovalue_class(input_args_str, params):
  input_arg_strs = input_args_str.split(',')
  output = AUTO_VALUE_CLASS_NAME + ".builder()"
  cleaned_arg_strs = [clean_input_arg(s) for s in input_arg_strs]

  for arg, param in zip(cleaned_arg_strs, params):
    output += "\n.set%s(%s)" % (upperfirst(param.name), arg)
  output += "\n.build()"
  return output


def clean_input_arg(s):
  if "*/" in s:
    s = s.split("*/", 1)[1]

  return s.strip()


def can_skip_arg(arg):
  return arg in ("false", "Optional.empty()")


def parse_args(cmd_args):
  description = __doc__.split("Copyright 2018")[0].strip()

  parser = argparse.ArgumentParser(
    description=description,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument("func_def_input_file", help="A file with the function definition")
  parser.add_argument("--output_autovalue_class", action="store_true")
  parser.add_argument("--convert_method_calls_in_test_file")
  parser.add_argument("--convert_call_site_file")

  args = parser.parse_args(cmd_args)
  return args


def main():
  args = parse_args(sys.argv[1:])

  app = App(args)
  sys.exit(app.run())


if __name__ == '__main__':
  main()
