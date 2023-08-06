from inspect import getfullargspec, unwrap

from django import VERSION as DJ_VERSION
from django import template
from django.template.library import parse_bits
from django.template.base import Context, NodeList

from .arg_tag import ArgNode, ArgAlreadyDefinedException
from .component import Component
from .media import add_media

import typing as t


def make_component_tag(
    component_cls: t.Type[Component], self_closed: bool
) -> t.Callable:
    component = component_cls()
    [_, *params], varargs, varkw, defaults, kwonly, kwonly_defaults, _ = getfullargspec(
        unwrap(component.context)
    )

    def parse_component(parser, token) -> ComponentNode:
        component_name, *bits = token.split_contents()

        if DJ_VERSION[0] > 1:
            args, kwargs = parse_bits(
                parser,
                bits,
                params,
                varargs,
                varkw,
                defaults,
                kwonly,
                kwonly_defaults,
                False,
                component_name,
            )
        else:
            args, kwargs = parse_bits(
                parser, bits, params, varargs, varkw, defaults, False, component_name,
            )
        if self_closed is False:
            nodelist = parser.parse((f"/{component_name}",))
            parser.delete_first_token()
        else:
            nodelist = NodeList()

        return ComponentNode(component, nodelist, args, kwargs)

    return parse_component


class ComponentNode(template.Node):
    def __init__(
        self,
        component: Component,
        nodelist: template.NodeList,
        args: t.List,
        kwargs: t.Dict,
    ):
        self.component = component
        self.args = args
        self.kwargs = kwargs
        self.nodelist = nodelist

    def render(self, context: Context) -> str:
        self.register_media(context)
        args, kwargs = self.get_resolved_arguments(context)
        child_nodes, args_tags = self.get_child_nodes_and_args_tags(context, kwargs)
        kwargs.update(args_tags)
        with context.push():
            component_context = self.component.context(*args, **kwargs)
            rendered = self.component.render(child_nodes, context, component_context)
        return rendered

    def register_media(self, context):
        add_media(context, self.component.media)

    def get_resolved_arguments(self, context):
        resolved_args = [var.resolve(context) for var in self.args]
        resolved_kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        return resolved_args, resolved_kwargs

    def get_child_nodes_and_args_tags(self, context, kwargs):
        child_nodes = NodeList()
        args_tags = {}
        for node in self.nodelist:
            if isinstance(node, ArgNode):
                arg_tag_name = node.name
                if arg_tag_name in kwargs:
                    raise ArgAlreadyDefinedException(
                        f"An argument named {arg_tag_name} is already defined for {self.component.__class__.__name__}"
                    )

                arg_rendered = node.render_arg_tag(context)
                if arg_tag_name in args_tags.keys():
                    if not isinstance(args_tags[arg_tag_name], list):
                        args_tags[arg_tag_name] = [args_tags[arg_tag_name]]
                    args_tags[arg_tag_name].append(arg_rendered)
                else:
                    args_tags[arg_tag_name] = arg_rendered
            else:
                child_nodes.append(node)
        return child_nodes, args_tags
